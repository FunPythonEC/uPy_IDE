# uPy_IDE (An attemp of making a MicroPython IDE)
Proyecto para desarrollar un IDE con opciones de flashear MicroPython en microcontroladores ESP.
Pronto se agregara un campo para edición y manejo del cli.

## Ejecución
Para ejecutar el script para el editor, debido a que todavia esta en su etapa de desarrollo, no es un ejecutable directamente. Antes para una ejecución precisa, es preferible la creación de un entorno virtual para poder instalar toga y ciertas dependencias que suelen ser necesarias.

Para ello ver los minimos requisitos aquí: https://github.com/pybee/toga/blob/master/README.rst

Una vez que ya se tengan los minimos requerimientos, y los establecido más abajo, basta con correr el siguiente comando afuera de la carpeta del directorio del proyecto.
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



