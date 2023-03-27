Dokumentacja robo-data-link
=============================

**Robot-data-link** to łącznik danych z różnych sensorów przeznaczony do współpracy z urządzeniami, komunikującymi się za pomocą interfejsu RS-232 lub TCP.


.. note::

   Projekt jest aktywnie rozwijany.


Requirements & libraries
=========================

* Python >=3.10.5
* `Marshmallow <https://github.com/marshmallow-code/marshmallow>`_ - an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes. In this project, marshmallow validates and converts the configuration file _moduleConfig.json to a Python object

.. code-block:: console

    $ pip install -U marshmallow

* `npyscreen <https://npyscreen.readthedocs.io>`_ - npyscreen is a python widget library and application framework for programming terminal or console applications. It is built on top of ncurses, which is part of the standard library.

.. code-block:: console

    $ pip install npyscreen

* `pySerial <https://pythonhosted.org/pyserial/>`_ - his module encapsulates the access for the serial port.

.. code-block:: console

    $ pip install pyserial


**Dokumentacja**

* `Sphinx <https://www.sphinx-doc.org>`_ - Sphinx makes it easy to create intelligent and beautiful documentation.

WINDOWS

.. code-block:: console
    
    $ pip install -U sphinx

LINUX

.. code-block:: console
    
    $ sudo apt-get install python3-sphinx

* `sphinx-design <https://pypi.org/project/sphinx_design/>`_ - A sphinx extension for designing beautiful, view size responsive web components.

.. code-block:: console
    
    $ pip install sphinx_design


* `sphinx-rtd-theme <https://pypi.org/project/sphinx-rtd-theme/>`_ - This Sphinx theme was designed to provide a great reader experience for documentation users on both desktop and mobile devices.

.. code-block:: console
    
    $ pip install sphinx-rtd-theme

**Build documentation:** 
.. code-block:: console
    
    $ cd docs
    $ sphinx-build -M html . _build/


Lista portów
=============

.. code-block:: console
    
    $ python -m serial.tools.list_ports -v

Contents
--------

.. toctree::
   :maxdepth: 2

   Home <self>
   configfile
   addDeviceToConfig
   api


Urządzenia
-----------

.. toctree::

   rplidar


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


