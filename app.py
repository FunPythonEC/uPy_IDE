import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
import os
import sys
import glob
import serial
import time
from uPyIDE import esptool

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
		box_style=Pack(direction=ROW,padding=10)

		self.portselect=toga.Selection(items=serial_ports())
		self.chipselect=toga.Selection(items=["ESP8266","ESP32"], on_select=self.update_selections)
		self.verselect=toga.Selection(items=["v1.8.7","v1.9.0","v1.9.1","v1.9.2","v1.9.3","v1.9.4","v1.10.0"])

		self.filelabel=toga.Label("No ha seleccionado ningun archivo")
		self.fname=None
		self.main_window.content=toga.Box(
			children=[

				toga.Box(style=box_style, children=[
					self.portselect,
					self.chipselect,
					self.verselect
					]),

				toga.Box(style=box_style, children=[
					toga.Button("Flashear",on_press=self.flash),
					toga.Button("Borrar flash/firmware",on_press=self.eraseflash),
					toga.Button("Actualizar puertos",on_press=self.update_ports)
					]),

				toga.Box(style=box_style, children=[
					toga.Button("Seleccionar archivo",on_press=self.action_open_file_dialog),
					self.filelabel,
					toga.Button("Grabar archivo en ESP", on_press=self.save_esp)
					])
				])
		self.main_window.show()


	def save_esp(self, button):
		command="python3.6 cli.py -p "+self.portselect.value+" put "+fname
		os.system(command)


	def flash(self,button):
		import os
		port=self.portselect.value
		chip=self.chipselect.value
		ver=self.verselect.value

		if chip == "ESP32":
			command = 'python3.6 esptool.py --chip esp32 --port '+port+' write_flash -z 0x1000 esp32/'+ver+'.bin'
			os.system(command)
		elif chip == "ESP8266":
			command = 'python3.6 esptool.py --port '+port+' --baud 460800 write_flash --flash_size=detect 0 esp8266/'+ver+'.bin'
			os.system(command)		

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
		import os
		port=self.portselect.value
		chip=self.chipselect.value
		if chip=='ESP32':
			command='python3.6 esptool.py --chip esp32 erase_flash'
			os.system(command)
		elif chip=='ESP8266':
			command='python3.6 esptool.py --port '+port+' erase_flash'
			os.system(command)

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
