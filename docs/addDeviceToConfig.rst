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
      "implementedBy": "DeviceModule",
      "numBuforBytes": 4
    },

gdzie pola ``name``, ``desc``, ``implementedBy`` to odpowiednio: nazwa modułu (taka sama jak nazwa w liście ``inputs``), opis modułu i nazwa klasy wątku, która implementuje logikę związaną z urządzeniem pomiarowym. Pole ``numBuforBytes`` to wielkość ramki (w bajtach). 

.. note:: 
    W ramce umieszczane są liczby ``int16``. Ze względu na łatwość konwersji na bajty, ramka jest reprezentowana przez tablice pakietu ``numpy``

Pozostałe pola zależą od urządzenia pomiarowego i pełnią rolę stałych konfiguracyjnych.

Poniżej przytoczono obiekt, którego klucz w pliku konfiguracyjnym to ``sensor``

.. code-block:: json-object

    "sensor":{
        "info": {
            "name": "sensor",
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



Implementacja wątku 
----------------------------

Wątek urządzenia I/O to klasa dziedzicząca po ``Thread`` i implementująca kilka metod. Jej szkielet to:

.. code-block:: python

    class SensorModule(Thread):

    def __init__(self,name,ioManager,outputSendEvent:Event):
        super().__init__()
        
        self.ioManager=ioManager
        self.name =name
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.closeEvent=ioManager.closeEvent
        self.outputSendEvent = outputSendEvent

        #wczytanie parametrów konfiguracyjnych, które ustawiono w pliku json

        #logi: glob.log.info("Thread %s create",self.name)

    def init(self):
        #instrukcje inicjalizujące

        if initIsOk
            return True 
        else
            return False 

    def run(self):
        while True:
            if self.closeEvent.is_set():
                self.afterClose()
                break
            if self.outputSendEvent.is_set():
                self.afterSendByOutput()

    def afterClose(self):
        self.ioManager.tui.updateStatus(self.name,"STOP")

    def afterSendByOutput(self):
        self.outputSendEvent.clear()