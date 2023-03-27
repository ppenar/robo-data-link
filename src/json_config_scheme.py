from marshmallow import Schema, fields,pre_load, ValidationError, validate, post_load
import utils, configModel

class JsonInfoScheme(Schema):
    """
        Klasa opisuje (z użyciem biblioteki marshmallow) schemat obiektu JSON, który jest przypisany do klucza info. Klucz info jest wymagany w opisie urządzeń wejściowych i wyjściowych. 

        Parametry
        ----------
            name : str
                [pole wymagane] nazwa modułu
            desc : str
                [pole wymagane] Opis moduły wyświetlany w TUI/GUI
            implementedBy : str
                [pole wymagane] nazwa klasy, która implementuje wątek I/O, który obsługuje opisywany moduł
            numBuforBytes: int
                [pole wymagane] liczba bajtów w buforze. Bufor to tablica numpy, w której typ danych to int16, dlatego
                bufor stanowi numBuforBytes/2 liczb. 

        .. code-block:: 
  
            "info":{
                "name": "Dspace",
                "desc": "Dspace desc",
                "implementedBy": "DspaceModule",
                "numBuforBytes": 16
                },
        """
    name = fields.Str(required=True, 
                      error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeStrInvalid")
        })
    desc = fields.Str(required=True, 
                      error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeStrInvalid")
        })
    implementedBy = fields.Str(required=True, 
                      error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeStrInvalid")
        })
    numBuforBytes = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    
    @post_load
    def makeObject(self, data, **kwargs):
        return configModel.Info(**data)

class JsonLeicaScheme(Schema):
    info = fields.Nested(JsonInfoScheme)
    ip = fields.IPv4(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIPInvalid")
        })
    port = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    mode = fields.Str(validate=validate.OneOf(utils.getLeicaModeList()),
                      required=True,
                      error_messages={
                        "required": utils.getErrorMsg("SchemeRequired")
                      })
    @post_load
    def makeObject(self, data, **kwargs):
        return configModel.Leica(**data)


class JsonLidarScheme(Schema):
    info = fields.Nested(JsonInfoScheme)
    port = fields.Str(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeStrInvalid")
        })
    baundrate = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    stepAngle = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    @post_load
    def makeObject(self, data, **kwargs):
        return configModel.Lidar(**data)
    

class JsonInputRandomScheme(Schema):
    info = fields.Nested(JsonInfoScheme)
    msSleepTime = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    @post_load
    def makeObject(self, data, **kwargs):
        return configModel.InputRandom(**data)


class JsonOutputDemoScheme(Schema):
    info = fields.Nested(JsonInfoScheme)
    msSleepTime = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    @post_load
    def makeObject(self, data, **kwargs):
        return configModel.OutputDemo(**data)


class JsonSerialScheme(Schema):
    info = fields.Nested(JsonInfoScheme)
    port = fields.Str(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeStrInvalid")
        })
    baundrate = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    join = fields.Boolean(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeBoolInvalid")
        })
    msSleepTime = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    @post_load
    def makeObject(self, data, **kwargs):
        return configModel.Serial(**data)
    
class JsonTcpScheme(Schema):
    info = fields.Nested(JsonInfoScheme)
    ip = fields.IPv4(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIPInvalid")
        })
    port = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    mode = fields.Str(validate=validate.OneOf(utils.getTcpModeList()),
                      required=True,
                      error_messages={
                        "required": utils.getErrorMsg("SchemeRequired")
                      })
    msSleepTime = fields.Integer(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeIntInvalid")
        })
    
    @post_load
    def makeObject(self, data, **kwargs):
        return configModel.Tcp(**data)

class JsonConfigScheme(Schema):

    profil = fields.Str(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeStrInvalid")
        })
    inputs=fields.List(fields.Str, 
                       required=True,
                       error_messages={
        "required": utils.getErrorMsg("SchemeRequired")
        })
    output = fields.Str(required=True, 
                        error_messages={
        "required": utils.getErrorMsg("SchemeRequired"),
        "invalid": utils.getErrorMsg("SchemeStrInvalid")
        })
    tcp = fields.Nested(JsonTcpScheme)
    serial = fields.Nested(JsonSerialScheme)
    lidar = fields.Nested(JsonLidarScheme)
    leica = fields.Nested(JsonLeicaScheme)
    inputrandom1 = fields.Nested(JsonInputRandomScheme)
    inputrandom2 = fields.Nested(JsonInputRandomScheme)
    
    @pre_load
    def checkDefineModuleConfig(self, data, **kwargs):
        if data["output"] not in data:
            raise ValidationError(utils.getErrorMsg("SchemeOutputModuleError"))
        
        for input in data["inputs"]:
            if input not in data:
                raise ValidationError(utils.getErrorMsg("SchemeInputModuleError"))
        return data 

    @post_load
    def makeObject(self, data, **kwargs):
        return configModel.ModuleConfig(**data)




     