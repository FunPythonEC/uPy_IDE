import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
import os
import sys
import glob
import serial

def serial_ports():
      
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
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
        except:
            pass
    return result

class uPyIDE(toga.App):

	def startup(self):

		self.main_window=toga.MainWindow(title=self.name,size=(640,400))

		label_style=Pack(flex=1,padding_right=24)
		box_style=Pack(direction=ROW,padding=10)

		global portselect
		global chipselect
		global verselect

		portselect=toga.Selection(items=None, on_select=self.updateslct)
		chipselect=toga.Selection(items=["ESP8266","ESP32"],on_select=self.updateslct)
		verselect=toga.Selection(items=["v1.8.7","v1.9.0","v1.9.1","v1.9.2","v1.9.3","v1.9.4","v1.10.0"])

		self.main_window.content=toga.Box(
			children=[

				toga.Box(style=box_style, children=[
					portselect,
					chipselect,
					verselect
					]),

				toga.Box(style=box_style, children=[
					toga.Button("Flashear",on_press=self.flash),
					toga.Button("Borrar flash/firmware",on_press=self.eraseflash),
					toga.Button("Actualizar",on_press=self.updatebtn)
					])
				])
		self.main_window.show()



	def flash(self,button):
		import os
		port=portselect.value
		chip=chipselect.value
		ver=verselect.value

		if chip == "ESP32":
			command = 'esptool.py --chip esp32 --port '+port+' write_flash -z 0x1000 esp32/'+ver+'.bin'
			os.system(command)
		elif chip == "ESP8266":
			command = 'esptool.py --port '+port+' --baud 15200 write_flash --flash_size=detect 0 esp8266/'+ver+'.bin'
			os.system(command)		

	def updateslct(self, selection):
		portlist = serial_ports()
		micro=chipselect.value
		if not portlist:
			pass
		else:
			portselect.items(portlist)

		if micro == "ESP32":
			versionlist=["v1.9.4","v1.10"]
		elif micro=="ESP8266":
			versionlist=["v1.8.7","v1.9.0","v1.9.1","v1.9.2","v1.9.3","v1.9.4","v1.10.0"]
		else:
			pass
		verselect.items(versionlist)

	def updatebtn(self, button):
		portlist = serial_ports()
		micro=chipselect.value
		print(portlist)
		if not portlist:
			pass
		else:
			portselect.items(items=portlist)

		if micro == "ESP32":
			versionlist=["v1.9.4","v1.10"]
		elif micro=="ESP8266":
			versionlist=["v1.8.7","v1.9.0","v1.9.1","v1.9.2","v1.9.3","v1.9.4","v1.10.0"]
		else:
			pass

		verselect.items(items=versionlist)

	def eraseflash(self,button):
		import os
		port=portselect.value
		chip=chipselect.value
		if chip=='ESP32':
			command='esptool.py --chip esp32 erase_flash'
			os.system(command)
		elif chip=='ESP8266':
			command='esptool.py --port '+port+' erase_flash'
			os.system(command)



def main():
	return uPyIDE("uPyIDE","org.funpython.upyide")