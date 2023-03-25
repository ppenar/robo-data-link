# robo-data-link

Application to connect multiple measuring devices.



# Requirements & libraries

* Python >=3.10.5
* [Marshmallow](https://github.com/marshmallow-code/marshmallow) - _an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes_. In this project, _marshmallow_ validates and converts the configuration file _moduleConfig.json_ to a Python object
* [npyscreen]  (https://npyscreen.readthedocs.io)
.. code-block:: console
    
    $ pip install npyscreen



# Dokumentacja

* [for Rasp]: sudo apt-get install python3-sphinx

Build: 

# Lista portów
.. code-block:: console
    
    $ python -m serial.tools.list_ports -v