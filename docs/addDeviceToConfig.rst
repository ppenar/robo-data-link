Dodawanie urządzenia pomiarowego
===================================

Dodanie obsługi nowego urządzenia pomiarowego składa się z dwóch etapów: przygotowanie konfiguracji oraz implementacja wątku. 

Przygotowanie konfiguracji
----------------------------

**Obiekt JSON**

Każde urządzenie pomiarowe będące wejściem do aplikacji jest reprezentowane w pliku konfiguracyjnym przez klucz z nazwą, reprezentującą dodawane urządzenie. Jego wartość to obiekt, który musi zawierać klucz ``info``, którego wartość to obiekt postaci

.. code-block:: json-object

   {
      "name": "device_name",
      "desc": "device desc",
      "implementedBy": "DeviceModule"
    },

gdzie pola ``name``, ``desc``, ``implementedBy`` to odpowiednio: nazwa modułu, opis modułu i nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym.

Pozostałe pola zależą od urządzenia pomiarowego i pełnią rolę stałych konfiguracyjnych.

Poniżej przytoczono obiekt, którego klucz w pliku konfiguracyjnym to ``sensor``

.. code-block:: json-object

    "sensor":{
        "info": {
            "name": "device_name",
            "desc": "device desc",
            "implementedBy": "DeviceModule"
       },
      "IP": "192.168.10.1",
      "port": 3333,
      "mode": "speed"
    }

Powyższy obiekt JSON, przypisany do klucza ``sensor``, należy dodać do pliku konfiguracyjnego, jeśli jednym z wejść aplikacji są dane, które pochodzą z tego urządzenia. Należy pamiętać, by do listy urządzeń wejściowych tj. ``inputs`` dodać wpis ``sensor``.
**Schemat konfiguracji i deserializacja**
Konfiguracja zapisana w pliku json jest widziana jako obiekt Pythona, co wymaga serializacji, którą zapewnia biblioteka `marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_. Dlatego by poprawnie odwzorować JSON w obiekcie konfiguracyjnym Python wymagana jest realizacja następujących kroków:

1. Dodanie schematu obiektu jako klasy dziedziczącej po klasie Schema z biblioteki marshmallow do pliku json_config_schema.js.
2. Dodanie pola w klasie JsonConfigScheme w pliku json_config_schema.js. Np.:

.. code-block:: python

    lidar = fields.Nested(JsonLidarScheme)

3. Dodanie klasy Python w pliku configModel.py, która reprezentuje obiekt JSON.
4. Dodanie pola reprezentującego urządzenie do klasy ConfigModel. **Dodanie odpowiedniego parametru w konstruktorze z wartością domyślą None**. Ma to na celu poprawną deserializacji obiektu JSON w przypadku, gdy moduł nie jest używany. 
