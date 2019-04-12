# uPy_IDE (An attemp of making a MicroPython IDE) :laughing:
Proyecto de desarrollo de un IDE con opciones de flashear MicroPython en microcontroladores ESP.
Pronto se agregara un campo simulador del REPL de MicroPython.

## Ejecución
Hasta ahora solo se ha creado un ejecutable que es para Linux. Sin embargo, el proyecto en general esta todavía en una etapa de desarrollo, por lo que tambien se puede correr el proyecto en si pero debe cumplirse ciertos requerimientos dependiendo del sistema operativo.

Para ello ver los minimos requisitos aquí: https://github.com/pybee/toga/blob/master/README.rst

Una vez que se tengan los requerimientos instalados y se haya clonado el repositorio localmente. Abrir una terminal fuera de la carpeta del proyecto y ejecutar uno de los proximos comandos:

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



