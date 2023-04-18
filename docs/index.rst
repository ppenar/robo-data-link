Dokumentacja robo-data-link
=============================

**Robot-data-link** to łącznik danych z różnych sensorów przeznaczony do współpracy z urządzeniami, komunikującymi się za pomocą interfejsu RS-232 lub TCP.


.. note::

   Projekt jest aktywnie rozwijany.


Wymagania & biblioteki
=========================

* Python >=3.10.5
* `Marshmallow <https://github.com/marshmallow-code/marshmallow>`_ - biblioteka ORM do konwersji złożonych typów danych, takich jak obiekty, z/do natywnych typów danych Pythona. W tym projekcie biblioteka *marshmallow* sprawdza poprawność i konwertuje plik konfiguracyjny moduleConfig*.json na obiekt Pythona.

.. code-block:: console

    $ pip install -U marshmallow

* `npyscreen <https://npyscreen.readthedocs.io>`_ - npyscreen to biblioteka widżetów do budowania aplikacji  konsolowych. Jest zbudowana na bazie biblioteki *ncurses*, która jest częścią biblioteki standardowej.

.. code-block:: console

    $ pip install npyscreen

* `pySerial <https://pythonhosted.org/pyserial/>`_ - moduł umożliwiający dostęp do portu szeregowego

.. code-block:: console

    $ pip install pyserial


**Dokumentacja**


* `Sphinx <https://www.sphinx-doc.org>`_ - Moduł do tworzenia dokumentacji

WINDOWS

.. code-block:: console
    
    $ pip install -U sphinx

LINUX

.. code-block:: console
    
    $ sudo apt-get install python3-sphinx

* `sphinx-design <https://pypi.org/project/sphinx_design/>`_ - Rozszerzenie do *Sphinx*

.. code-block:: console
    
    $ pip install sphinx_design


* `sphinx-rtd-theme <https://pypi.org/project/sphinx-rtd-theme/>`_ -  Rozszerzenie do *Sphinx*

.. code-block:: console
    
    $ pip install sphinx-rtd-theme

**Build:** 

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


