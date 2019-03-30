# uPy_IDE (An attemp of making a MicroPython IDE) :laughing:
Proyecto para desarrollar un IDE con opciones de flashear MicroPython en microcontroladores ESP.
Pronto se agregara un campo para edición y manejo del cli.

## Ejecución
Para poder ejecutar el script, debido a que este se encuentra en etapa de desarrollo, aun no es ejecutable directamente. Para una mejor ejecución es preferible primero la creación de un entorno virtual en el cual pueda instalar toga y ciertas dependencias necesrias. 

Para ello ver los minimos requisitos aquí: https://github.com/pybee/toga/blob/master/README.rst

Una vez, se tengan los requerimientos minimos o los establecido para trabajar en entorno virtual(Descritos más adelante), basta con correr el siguiente comando afuera de la carpeta del directorio del proyecto.
`python -m uPy_IDE`
o
`python3 -m uPy_IDE`
### Sin entorno virtual
~~~~ bash
sudo pip3 install --pre toga
~~~~
### Con entorno virtual
~~~~ bash
python3 -m venv venv
source venv/bin/activate
pip install --pre toga
pip install pyserial
pip install python-dotenv
~~~~



