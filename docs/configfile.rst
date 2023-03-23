Plik konfiguracyjny
====================

Plik konfiguracyjny definiuje działanie programu, który można traktować, jako czarną skrzynkę do przetwarzania danych z wielu źródeł. **Wejścia** to moduły, które są wątkami Pythona obsługującymi połączenie z urządzeniami dostarczającymi dane. Takie podejście pozwala na wygodną implementacje logiki, niezależność czasową w ramach wątku i skalowalność rozwiązania. Pozyskane dane, poprzez wspólny bufor, trafiają na **wyjście**, jako strumień bajtów transmitowany w połączeniu szeregowym bądź jako dane wysyłane poprzez TCP/IP.


Przykład
---------

Konfiguracje programu, czyli definicje wejść i wyjścia zapisano w pliku JSON. Jego przykład przytoczono poniżej

.. code-block:: 
  
  {
  "profil":"name",
  "inputs": ["lidar","leica"],
  "output": "dspace",
  "dspace":{
    "info":{
      "name": "Dspace",
      "desc": "Dspace desc",
      "implementedBy": "DspaceModule",
      numBuforBytes: 16
    },
    "port": "COM11",
    "baundrate": 9600,
    "join": true,
    "msSleepTime": 50    
  },
  "lidar":{
    "info":{
      "name": "Lidar",
      "desc": "Lidar desc",
      "implementedBy": "LidarModule",
      "numBuforBytes": 16
    },
    "port": "COM12",
    "baundrate": 9600
  },
  "leica":{
    "info":{
      "name": "Leica",
      "desc": "Leica desc",
      "implementedBy": "LeicaModule",
      "numBuforBytes": 16
    },
    "IP": "123.10.50.1",
    "port": "8001",
    "mode": "Stationary"
  }
  }

Poprawność struktury i składni obiektu konfiguracyjnego JSON jest oceniana na podstawie schematu generowanego w przez bibliotekę   `marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_.


Opis pliku 
------------
Pole ``profil`` definiuje nazwę profilu aplikacji. Nazwa to ciąg znaków.

Lista ``inputs`` określa listę aktywnych wejść aplikacji które są reprezentowane przez ciągi znakowe. Ich porządek określa kolejność wysyłania (co może poprzedzić ich połączenie) danych przez wyjście. Wszystkie wymienione w liście nazwy muszą być zdefiniowane w pliku jako klucze JSON, których wartości to obiekty, w których zdefiniowano konfiguracje odpowiedniego wyjścia. Obowiązkowym polem takiego obiektu, jest Pole ``info``, którego wartość to obiekt zawierający klucze: ``name``, ``desc``, ``implementedBy``, ``numBuforBytes``, których wartości to odpowiednio: nazwa modułu, opis modułu, nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym które reprezentuje oraz wielkość bufora.


Wartość pola ``output`` definiuje rodzaj wyjścia. Jego nazwa musi być taka sama, jak nazwa klucza JSON, którego wartość to obiekt zawierający konfiguracje wyjścia.  W tym przypadku wymaganym polem, podobnie jak w przypadku wejść, jest ``info``, niemniej parametr ``numBuforBytes`` nie ma znaczenia ja jego występowanie podyktowane jest unifikacją obiektu przypisanego do pola ``info``.

Kolejne klucze JSON odpowiadają nazwą wejść i wyjścia a ich wartości to obiekty z konfiguracją urządzeń, z którymi są związane. 

* ``DSpace`` 

Poniżej przytoczono obiekt konfigurujący dla karty pomiarowej Dspace. W pliku konfiguracyjnym który przytoczono powyżej, karta DSpace jest związana w wyjściem. To do niej transmitowane są dane (z wykorzystaniem łącza szeregowego).

.. code-block:: json-object

   "dspace":{
    "info":{
      "name": "Dspace",
      "desc": "Dspace desc",
      "implementedBy": "DspaceModule",
      "numBuforBytes": 16
    },
    "port": "COM11",
    "baundrate": 9600,
    "join": true,
    "msSleepTime": 50    
  }

Obiekt konfigurujący procesor sygnałowy DSpace zawiera:
  * ``info`` to klucz zawierający obiekt, którego pola to: ``name``, ``desc``, ``implementedBy``, ``numBuforBytes``. Ich wartości to ciągi znakowe, których znaczenie to odpowiednio: nazwa modułu, opis modułu, nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym które reprezentuje wątek. Wartość parametru ``numBuforBytes`` w tym przypadku (czyli dla wyjścia) nie ma znaczenia.
  *  ``port`` którego wartość to ciąg znakowy, który określa nazwę portu szeregowego w systemie, 
  *  ``baundrate`` to liczba całkowita określająca prędkość w komunikacji szeregowej. 
  *  ``join`` może przyjmować wartości 0 lub 1 i określa, czy dane pochodzące od wielu urządzeń wejściowym mają być wysyłane jako jeden strumień bajtów  (wartość 1) czy jako kolejne strumienie bajtów (wartość 0)
  *  ``msSleepTime`` to pole którego wartość określa liczbę milisekund przerwy w wywołaniu wątku wysyłającego dane do kary sygnałowej. To pozwala na dostosowanie szybkości przesyłania kolejnych danych do procesowa sygnałowego.

  
* ``Lidar`` 

Obiekt konfiguracyjny związany z urządzeniem :doc:`rplidar` ma postać 

.. code-block:: json-object

  "lidar":{
    "info":{
      "name": "Lidar",
      "desc": "Lidar desc",
      "implementedBy": "LidarModule",
      "numBuforBytes": 16
    },
    "port": "COM12",
    "baundrate": 9600
  }
      
gdzie:
  * ``info`` to klucz zawierający obiekt, którego pola to: ``name``, ``desc``, ``implementedBy`` i ``numBuforBytes``. Ich wartości to ciągi znakowe, których znaczenie to odpowiednio: nazwa modułu, opis modułu i nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym które reprezentuje wątek. Ostatni parametr tj. ``numBuforBytes`` określa wielkość bufora związanego z tym wejściem.
  *  ``port`` którego wartość to ciąg znakowy, który określa nazwę portu szeregowego w systemie, 
  *  ``baundrate`` to liczba całkowita określająca prędkość w komunikacji szeregowej. \



* ``Leica`` 


Obiekt konfiguracyjny związany z trackerem laserowym Leica ma postać


.. code-block:: json-object

  "leica":{
    "info":{
      "name": "Leica",
      "desc": "Leica desc",
      "implementedBy": "LeicaModule",
      "numBuforBytes": 16
    },
    "IP": "123.10.50.1",
    "port": "8001",
    "mode": "Stationary"

gdzie 
  * ``info`` to klucz zawierający obiekt, którego pola to: ``name``, ``desc``, ``implementedBy``. Ich wartości to ciągi znakowe, których znaczenie to odpowiednio: nazwa modułu, opis modułu i nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym które reprezentuje wątek. Ostatni parametr tj. ``numBuforBytes`` określa wielkość bufora związanego z tym wejściem.
  *  ``IP``, ``port`` adres i port trackera laserowego
  *  ``mode`` tryb pracy trackera.

