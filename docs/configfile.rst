Plik konfiguracyjny
====================

Plik konfiguracyjny definiuje działanie programu, który można traktować jak czarną skrzynkę do przetwarzania danych z wielu źródeł. **Wejścia** to moduły, które są wątkami Pythona obsługującymi połączenie z urządzeniami dostarczającymi dane. Takie podejście pozwala na wygodną implementacje logiki, niezależność czasową w ramach wątku i skalowalność rozwiązania rozumianą jako dodawanie nowych urządzeń wejścia. Pozyskane dane, poprzez współdzielony bufor, trafiają na **wyjście**, jako strumień bajtów transmitowany poprzez port szeregowy bądź jako dane wysyłane z użyciem TCP/IP.

W projekcie zdefiniowano:

* ``moduleConfigLidarSerial.json`` - wejściem programu jest lidar RPLIDAR a wyjście to port szeregowy.
* ``moduleConfigRandomOutputTCP.json`` - wejściem programu jest generator liczb losowych (`numpy.random.randint <https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html>`_), który zapełnia 8-bajtową ramkę liczbami typu ``int`` w zakresie[0,100). Jego wyjście stanowi serwer TCP który na porcie 50001 przesyła dane (do podłączonych klientów) co zdefiniowany (klucz ``msSleepTime`` obiektu ``tcp``) kwant czasu.
* ``moduleConfigRandomSerial.json`` - wejściem programu jest generator liczb losowych (`numpy.random.randint <https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html>`_), który zapełnia 8-bajtową ramkę liczbami typu ``int`` w zakresie[0,100). Jego wyjście to port szeregowy, na który przesyłane są dane z wyjść co określony (klucz ``msSleepTime`` obiektu ``serial``) kwant czasu.
* ``moduleConfigViconSerial.json`` - wejściem programu jest system motion capture firmy Vicon. Jego wyjście to port szeregowy, na który przesyłane są dane z wyjść co określony (klucz ``msSleepTime`` obiektu ``serial``) kwant czasu.

.. note:: 

  Zmiana używanego pliku konfiguracyjnego jest realizowana poprzez modyfikacje wartości klucza ``FileName`` sekcji ``CONFIG_JSON`` pliku konfiguracyjnego ``config.ini`` 

Przykład
---------

Jego przykład pliku konfiguracyjnego przytoczono poniżej

.. code-block::
  
  {
    "profil":"Profil_demo",
    "inputs": ["inputrandom1","inputrandom2"],
    "output": "tcp"
    "tcp":{
    "info":{
      "name": "output_tcp",
      "desc": "Output TCP",
      "implementedBy": "TcpOutput",
      "numBuforBytes": 8
    },
    "msSleepTime": 2000,
    "ip": "127.0.0.1",   
    "port": 50001,
    "mode": "Continous"

  },
  "inputrandom1":{
    "info":{
      "name": "inputrandom1",
      "desc": "Input Random 1 desc",
      "implementedBy": "InputRandom",
      "numBuforBytes": 4
    },
    "msSleepTime": 2000
  },
  "inputrandom2":{
    "info":{
      "name": "inputrandom2",
      "desc": "Input Random 2 desc",
      "implementedBy": "InputRandom",
      "numBuforBytes": 4
    },
    "msSleepTime": 2000
  }
  }

Poprawność struktury i składni obiektu konfiguracyjnego JSON jest oceniana na podstawie schematu generowanego w przez bibliotekę   `marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_.


Opis pliku 
------------
Pole ``profil`` definiuje nazwę profilu aplikacji. Nazwa to ciąg znaków.

Lista ``inputs`` określa listę aktywnych wejść aplikacji które są reprezentowane przez ciągi znakowe. Ich porządek określa kolejność wysyłania (co może poprzedzić ich połączenie w jedną ramkę) danych przez wyjście. Wszystkie wymienione w liście nazwy muszą być zdefiniowane w pliku jako klucze JSON, których wartości to obiekty. W tych zdefiniowano konfiguracje odpowiedniego wyjścia. Obowiązkowym polem takiego obiektu, jest Pole ``info``, którego wartość to obiekt zawierający klucze: ``name``, ``desc``, ``implementedBy``, ``numBuforBytes``, których wartości to odpowiednio: nazwa modułu (**taka sama jak w liście wejść**) opis modułu, nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym które reprezentuje oraz wielkość bufora.


Wartość pola ``output`` definiuje rodzaj wyjścia. Jego nazwa musi być taka sama, jak nazwa klucza JSON, którego wartość to obiekt zawierający konfiguracje wyjścia.  W tym przypadku wymaganym polem, podobnie jak w przypadku wejść, jest ``info``, niemniej parametr ``numBuforBytes`` nie ma znaczenia, a jego występowanie podyktowane jest unifikacją obiektu przypisanego do pola ``info``. Z uwagi na założenie, że robo-data-link posiada tylko jedno wyjście, wartość pola ``name`` może być dowolna.

Kolejne klucze JSON oto obiekty z konfiguracją urządzeń I/O, z którymi są związane. 

* ``Serial`` 

Poniżej przytoczono obiekt konfigurujący dla wyjścia, którym jest port szeregowy.

.. code-block:: json-object

   "serial":{
    "info":{
      "name": "serial",
      "desc": "serial Dspace desc",
      "implementedBy": "SerialOutput",
      "numBuforBytes": 18
    },
    "port": "/dev/ttyUSB1",
    "baundrate": 115200,
    "join": true,
    "msSleepTime": 10    
  }

Obiekt konfigurujący port szeregowy zawiera:
  * ``info`` to klucz zawierający obiekt, którego pola to: ``name``, ``desc``, ``implementedBy``, ``numBuforBytes``. Ich wartości to ciągi znakowe, których znaczenie to odpowiednio: nazwa modułu, opis modułu, nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym które reprezentuje wątek. Wartość parametru ``numBuforBytes`` w tym przypadku (czyli dla wyjścia) nie ma znaczenia.  Choć dla porządku wartość tego klucza powinna być równa sumie długości ramek wejść.
  *  ``port`` wartość tego klucza to ciąg znakowy, który określa nazwę portu szeregowego w systemie. Dla systemów Linux ``/dev/ttyUSBx``, dla Windows ``COMx`` 
  *  ``baundrate`` to liczba całkowita określająca prędkość w komunikacji szeregowej. 
  *  ``join`` może przyjmować wartości ``true`` lub ``false`` i określa, czy dane pochodzące od wielu urządzeń wejściowym mają być wysyłane jako jeden strumień bajtów  (wartość 1) czy jako kolejne strumienie bajtów (wartość 0)
  *  ``msSleepTime`` to pole którego wartość określa liczbę milisekund przerwy w wywołaniu wątku wysyłającego dane do kary sygnałowej. To pozwala na dostosowanie szybkości przesyłania kolejnych danych do procesowa sygnałowego.

  
* ``Lidar`` 

Obiekt konfiguracyjny związany z urządzeniem :doc:`rplidar` ma postać 

.. code-block:: json-object

  "lidar":{
    "info":{
      "name": "lidar",
      "desc": "Lidar desc",
      "implementedBy": "LidarModule",
      "numBuforBytes": 18
    },
    "port": "/dev/ttyUSB0",
    "baundrate": 256000,
    "stepAngle": 5
  }
      
gdzie:
  * ``info`` to klucz zawierający obiekt, którego pola to: ``name``, ``desc``, ``implementedBy`` i ``numBuforBytes``. Ich wartości to ciągi znakowe, których znaczenie to odpowiednio: nazwa modułu, opis modułu i nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym które reprezentuje wątek. Ostatni parametr tj. ``numBuforBytes`` określa wielkość bufora związanego z tym wejściem.
  *  ``port`` którego wartość to ciąg znakowy, który określa nazwę portu szeregowego w systemie, 
  *  ``baundrate`` to liczba całkowita określająca prędkość w komunikacji szeregowej. 
  *  ``stepAngle`` informacje z Lidara o odległości będą przesyłane dla tych kątów, które stanowią wielokrotnośc wartości tego pola.
  



* ``Vicon`` 


Obiekt konfiguracyjny systemu motion capture Vicon:


.. code-block:: json-object

  "vicon":{
    "info":{
      "name": "vicon",
      "desc": "Vicon desc",
      "implementedBy": "ViconModule",
      "numBuforBytes": 14
    },
    "remoteIp": "192.168.10.1",   
    "port": 51001,
    "size": 256,
    "gainRot": 100,
    "msSleepTime": 2000
    
  }

gdzie 
  * ``info`` to klucz zawierający obiekt, którego pola to: ``name``, ``desc``, ``implementedBy``. Ich wartości to ciągi znakowe, których znaczenie to odpowiednio: nazwa modułu, opis modułu i nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym które reprezentuje wątek. Ostatni parametr tj. ``numBuforBytes`` określa wielkość bufora związanego z tym wejściem.
  *  ``remoteIP``, ``port`` adres i port, na którym Vicon Tracker transmituje informacje o położeniu obiektu jako UDP Stream.
  *  ``size`` wielkość ramki w strumieniu UDP
  *  ``gainRot`` mnożnik wartości rotacji śledzonego obiektu
  *  ``msSleepTime`` to pole którego wartość określa liczbę milisekund przerwy w wywołaniu wątku.

