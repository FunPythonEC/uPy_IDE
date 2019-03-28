import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
import os
import sys
import glob
import serial
import time
import uPy_IDE.esptool as esptool

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

		#switchs
		self.switchdio=toga.Switch('DIO', is_on=False, style=Pack(padding_left=10,padding_top=5))

		self.filelabel=toga.Label("No ha seleccionado ningun archivo", style=Pack(padding=2))
		self.fname=None
		self.main_window.content=toga.Box(
			children=[
				toga.Box(style=box_style_verti, children=[

					toga.Box(style=Pack(direction=ROW,padding_left=25), children=[
						self.portselect,
						self.chipselect,
						self.verselect,
						self.switchdio
						]),

					toga.Box(style=Pack(direction=COLUMN,padding_top=7), children=[
						toga.Button("Seleccionar archivo", on_press=self.action_open_file_dialog, style=Pack(padding_top=15,padding_left=2)),
						self.filelabel,
						toga.Button("Grabar archivo en ESP", on_press=self.save_to_esp, style=Pack(padding=2))
						])
					]),
				toga.Box(style=box_style_verti, children=[
					toga.Button("Flashear",on_press=self.flash),
					toga.Button("Borrar flash/firmware",on_press=self.eraseflash),
					toga.Button("Actualizar puertos",on_press=self.update_ports)
					])
				])

		self.main_window.show()


	def save_to_esp(self, button):
		from uPy_IDE.pyboard import Pyboard
		from uPy_IDE import cli
		eboard=Pyboard(self.portselect.value)
		cli.put(self.fname,board=eboard)


	def flash(self,button):
		port=self.portselect.value
		chip=self.chipselect.value
		ver=self.verselect.value

		if chip == "ESP32":
			esptool.main(["--chip","esp32","--port",self.portselect.value,"write_flash","-z","0x1000","esp32/"+ver+'.bin'])
		elif chip == "ESP8266":
			if self.switchdio.get_is_on:
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

	def action_open_file_dialog(self, widget):
		try:
			self.fname = self.main_window.open_file_dialog(
				title="Open file with Toga",
				)
			print(self.fname)
		except ValueError:
			print("ha ocurrido un error")
		self.filelabel.text="Archivo seleccionado: "+self.fname.split("/")[-1]

def main():
	return uPyIDE("uPyIDE","org.funpython.upyide")
