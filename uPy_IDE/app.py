import glob
import os
import sys
import time

import serial
import toga
import uPy_IDE.esptool as esptool
from toga.constants import COLUMN, ROW
from toga.style.pack import *

# TODO: Exportar un ejecutable de Windows

# Correr en un proceso aparte para que no se congele la UI
def run_in_process(self, button, code_to_run):
	import timeit
	elapsed_time = timeit.timeit(code_to_run, number=1) # just to save it somewhere
	return elapsed_time


def serial_ports():
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result

class uPyIDE(toga.App):

	def startup(self):

		self.main_window=toga.MainWindow(title=self.name,size=(640,400))

		label_style=Pack(flex=1,padding_right=24)
		box_style_horiz=Pack(direction=ROW,padding=15)
		box_style_verti=Pack(direction=COLUMN,padding=15)

		#selections
		self.portselect=toga.Selection(items=serial_ports())
		self.chipselect=toga.Selection(items=["ESP8266","ESP32"], on_select=self.update_selections)
		self.verselect=toga.Selection(items=["v1.8.7","v1.9.0","v1.9.1","v1.9.2","v1.9.3","v1.9.4","v1.10.0"])

		#puerto
		self.port = None
		self.port_open=False

		#switchs
		self.switchdio=toga.Switch('DIO', is_on=False, style=Pack(padding_left=10,padding_top=5))

		#textinputs
		self.textfile=toga.TextInput(style=Pack(flex=1,width=200))
		self.commandesp=toga.TextInput(style=Pack(flex=1,width=450))

		#intento de terminal
		self.textterminal=toga.MultilineTextInput(id='terminal')

		#textoutputs
		self.textoutputs=toga.MultilineTextInput(id='output')


		self.filelabel=toga.Label("No ha seleccionado ningun archivo", style=Pack(padding=2))
		self.fname=None
		# definir los hijos del main box afuera del main box
		left_box = toga.Box(style=box_style_verti)
		left_box.add(toga.Box(style=Pack(direction=ROW,padding_left=25), children=[
						self.portselect,
						self.chipselect,
						self.verselect,
						self.switchdio
						]))
		left_box.add(toga.Box(style=Pack(direction=COLUMN,padding_top=7), children=[
						toga.Button("Ver archivos en ESP", on_press=self.read_files, style=Pack(padding_top=15,padding_left=2)),
						toga.Button("Seleccionar archivo", on_press=self.action_open_file_dialog, style=Pack(padding=2)),
						self.filelabel,
						toga.Button("Ejecutar archivo en ESP", on_press=self.run_in_esp, style=Pack(padding=2)),
						toga.Button("Grabar archivo en ESP", on_press=self.save_to_esp, style=Pack(padding=2)),
						self.textfile,
						toga.Button("Borrar archivo de ESP", on_press=self.erase_from_esp, style=Pack(padding=2)),
						toga.Button("Obtener archivo de ESP", on_press=self.get_file_esp, style=Pack(padding=2)),
						self.textoutputs
						]))

		# Cambio en la estructura de los boxes para que funcione el rendering de los hijos en Windows, el bug es propio de toga al momento de presentar los boxes
		# Agregar hijos de right_box
		# right_box = toga.Box(style=box_style_verti)
		# right_box.add(toga.Button("Flashear",on_press=self.flash, style=Pack(padding=2)))
		# right_box.add(toga.Button("Borrar flash/firmware",on_press=self.eraseflash, style=Pack(padding=2)))
		# right_box.add(toga.Button("Actualizar puertos",on_press=self.update_ports, style=Pack(padding=2)))
		# right_box.add(toga.Button("Abrir puerto", on_press=self.open_port, style=Pack(padding=2)))
		# right_box.add(self.textterminal)
		# right_box.add(toga.Box(style=Pack(direction=ROW,padding_top=7), children=[
		# 				self.commandesp,
		# 				toga.Button("Enviar comando", on_press=self.send_command, style=Pack(padding=2))
		# 				])
		# 			)

		left_box.add(toga.Button("Flashear",on_press=self.flash, style=Pack(padding=2)))
		left_box.add(toga.Button("Borrar flash/firmware",on_press=self.eraseflash, style=Pack(padding=2)))
		left_box.add(toga.Button("Actualizar puertos",on_press=self.update_ports, style=Pack(padding=2)))
		left_box.add(toga.Button("Abrir puerto", on_press=self.open_port, style=Pack(padding=2)))
		left_box.add(self.textterminal)
		left_box.add(toga.Box(style=Pack(direction=ROW,padding_top=7), children=[
						self.commandesp,
						toga.Button("Enviar comando", on_press=self.send_command, style=Pack(padding=2))
						])
					)
		
		container = toga.Box()
		container.add(left_box)
		# container.add(right_box)

		self.main_window.content = container

		self.main_window.show()


	# TODO: hacer que los metodos inernos sean multi-procesos
	# metodos para la parte de ampy
	def read_files(self,button):
		from uPy_IDE.pyboard import Pyboard
		from uPy_IDE import cli
		from uPy_IDE import files

		eboard=files.Files(Pyboard(self.portselect.value))
		filesesp=eboard.ls()
		print(filesesp)
		lstext=""
		for f in filesesp:
			lstext=lstext+f+"\n"
		self.textoutputs.clear
		self.textoutputs.value=lstext

	def action_open_file_dialog(self, widget):
		try:
			self.fname = self.main_window.open_file_dialog(
				title="Open file with Toga",
				)
			print(self.fname)
		except ValueError:
			print("ha ocurrido un error")
		self.filelabel.text="Archivo seleccionado: "+self.fname.split("/")[-1]

	def run_in_esp_thread(self, archiv, disp, terp):
		import uPy_IDE.pyboard as pyboard
		self.textterminal.clear()		
		pyboard.execfile(archiv, device=disp,terminal=terp)

	def run_in_esp(self,button):
		import threading
		runespthread = threading.Thread(target=self.run_in_esp_thread, args=(self.fname, self.portselect.value, self.textterminal))
		runespthread.start()

	def save_to_esp(self, button):
		from uPy_IDE.pyboard import Pyboard
		from uPy_IDE import cli
		eboard=Pyboard(self.portselect.value)
		cli.put(self.fname,board=eboard)

	def erase_from_esp(self,button):
		from uPy_IDE.pyboard import Pyboard
		import uPy_IDE.files as files
		eboard=files.Files(Pyboard(self.portselect.value))
		eboard.rm(self.textfile.value)

	def get_file_esp(self,button):
		from uPy_IDE.pyboard import Pyboard
		import uPy_IDE.files as files
		eboard=files.Files(Pyboard(self.portselect.value))
		fdata=eboard.get(self.textfile.value)
		self.textterminal.clear()
		self.textterminal.value=fdata

#======================================SOLO MANEJO DE PUERTO========================================================


	def open_port(self,button):
		from uPy_IDE.pyboard import Pyboard
		if not self.port_open:
			self.btnport.label="Cerrar puerto"
			self.port_open=True
			self.textterminal.clear()
			self.port=Pyboard(self.portselect.value)
			self.port.enter_raw_repl()
			read_port(self.port, self.port_open)
		else:
			self.btnport.label="Abrir puerto"
			self.port_open=False
			self.port.exit_raw_repl()
		

	def send_command(self,button):
		if self.port_open:
			print(self.commandesp.value)
			self.port.send(self.commandesp.value)

#===================================================================================================================		
	#metodos para la parte de esptool
	def flash(self,button):
		port=self.portselect.value
		chip=self.chipselect.value
		ver=self.verselect.value

		if chip == "ESP32":
			esptool.main(["--chip","esp32","--port",self.portselect.value,"write_flash","-z","0x1000","uPy_IDE/esp32/"+ver+'.bin'])
		elif chip == "ESP8266":
			if self.switchdio.is_on:
				esptool.main(["--port",self.portselect.value,"--baud","460800","write_flash","--flash_size=detect","0","uPy_IDE/esp8266/"+ver+'.bin'])		
			else:
				esptool.main(["--port",self.portselect.value,"--baud","460800","write_flash","--flash_size=detect","-fm","dio","0","uPy_IDE/esp8266/"+ver+'.bin'])		

	def update_ports(self, button):
		portlist = serial_ports()
		if not portlist:
			pass
		else:
			self.portselect.items = portlist

	def update_selections(self,button):
		micro=self.chipselect.value
		if micro == "ESP32":
			versionlist=["v1.9.4","v1.10"]
		elif micro=="ESP8266":
			versionlist=["v1.8.7","v1.9.0","v1.9.1","v1.9.2","v1.9.3","v1.9.4","v1.10.0"]
		else:
			pass
		self.verselect.items = versionlist
		

	def eraseflash(self,button):
		
		port=self.portselect.value
		chip=self.chipselect.value
		if chip=='ESP32':
			esptool.main(["-p",self.portselect.value,"erase_flash"])
		elif chip=='ESP8266':
			esptool.main(["-p",self.portselect.value,"erase_flash"])

def read_port_thread(port,port_status):
	while True:
		if port_status:
			ans=port.read_until(1, b'\x04', timeout=10, data_consumer=None)
			print(ans)

def read_port(port, portstatus):
	import threading
	runportthread = threading.Thread(target=read_port_thread, args=(port, portstatus))
	runportthread.start()

def main():
	return uPyIDE("uPyIDE","org.funpython.upyide")
