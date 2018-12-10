#librerias importadas necesarias de kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.base import runTouchApp
from kivy.metrics import dp
from serialports import serial_ports

#se forma la clase en la que se da forma a la interfaz
class AppPrincipal(App):

    def setOrientation(self, orient):
        self.orient = 'vertical'
    
    def build(self):
        
        #se definen las funciones que hace esptool para que luego sean utilizadas como flasheo() y borrarflash()
        def flasheo(instance):
            import os
            p=puertosbtn.text
            chip=microbtn.text
            if chip=='ESP32':
                command='esptool.py --chip esp32 --port '+p+' write_flash -z 0x1000 esp32v1.9.4.bin'
                os.system(command32)
            elif chip=='ESP8266':
                command='esptool.py --port '+p+' --baud 115200 write_flash --flash_size=detect 0 esp8266v1.9.4.bin'

        def borrarflash(instance):
            import os
            p=puertosbtn.text
            chip=microbtn.text
            if chip=='ESP32':
                command='esptool.py --chip esp32 erase_flash'
                os.system(command32)
            elif chip=='ESP8266':
                command='esptool.py --port '+p+' erase_flash'

        #se define el layout principal para poder agregar los diferentes campos como datos y opcion
        main_layout = BoxLayout(padding=10, orientation='vertical')

        
        datos = BoxLayout(padding=10, orientation='horizontal') #en datos se especifica todo lo necesario para manejar el microcontrolador, como version y puerto
        opcion = BoxLayout(padding=10, orientation='horizontal') #opcion tiene los distintos botones para escoger que accion se quiere hacer con el microcontrolador
        
        #se define los distintos DropDowns, como listas depegables en las que se podra escoger los distintos parametros para manejar el microcontroladores
        #se establece el dropdown para los puertos disponibles, estos son dinamicos, y cambian cada vez que se inicia el programa dependiendo de los dispositivos conectados
        puertosdb=DropDown()
        portlist=serial_ports()
        portlist.append('Ninguno')
        for i in portlist:
            btn= Button(text=i,size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn:puertosdb.select(btn.text))
            puertosdb.add_widget(btn)
        
        #dropdown para escoger que tipo de microcontrolador se quiere manejar, en este caso son quemados, que por default estaran ESP32 y ESP8266
        microdb=DropDown()
        microlist=['ESP32', 'ESP8266']
        for i in microlist:
            btn= Button(text=i,size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn:microdb.select(btn.text))
            microdb.add_widget(btn)

        #se especifican los distintos botones que ayudaran a escoger la accion que se quiere realizar
        flashbtn=Button(text='Flashear', size_hint=(None,None))#se usa para quemar micropython en el microcontrolador
        borrarbtn=Button(text='Borrar flash/firmware', size_hint=(None,None))#borra el firmware actual del microcontrolador

        #estos botones son necesarios para poder combinarlos con los dropdowns, ya que de esta manera se forma un combobox, que no esta implementado totalmente todavia en kivy
        puertosbtn=Button(text='Escoja Puerto', size_hint=(None,None))#
        microbtn=Button(text='Escoja Microcontrolador', size_hint=(None,None))

        #se utiliza el metodo bind de los botones para anexarlos a un metodo o funcion cuando sean presionados
        flashbtn.bind(on_press=flasheo)
        borrarbtn.bind(on_press=borrarflash)

        #para el caso de los dropdowns, es necesario especificar que los botones contengan a estos, y que se abran cuando el boton sea presionado
        puertosbtn.bind(on_release=puertosdb.open)
        microbtn.bind(on_release=microdb.open)
        
        #especificamos el tamano de los widgets agregados
        puertosbtn.size=dp(200),dp(150)
        microbtn.size=dp(200),dp(150)
        flashbtn.size=dp(200),dp(100)
        borrarbtn.size=dp(200),dp(100)

        #se agregan los comboboxes/dropdowns creados al layout datos donde se podra especificar el puerto y tipo de microcontrolador
        datos.add_widget(puertosbtn)
        datos.add_widget(microbtn)

        #se agregan los botones de flasheo y borrar flash
        opcion.add_widget(flashbtn)
        opcion.add_widget(borrarbtn)
        
        #finalmente se agregan los otros layouts al layout principal
        main_layout.add_widget(datos)
        main_layout.add_widget(opcion)

        #se especfica a los dropdown que funcionen como botones
        puertosdb.bind(on_select=lambda instance, x: setattr(puertosbtn, 'text', x))
        microdb.bind(on_select=lambda instance, x: setattr(microbtn, 'text', x))

        return main_layout

if __name__ == "__main__":
    app = AppPrincipal()
    app.run()