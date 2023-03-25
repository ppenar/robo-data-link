import robo_data_globals as glob
import utils
from robo_data_io import RoboDataIO
from marshmallow import ValidationError
from tui import TuiRoboDataLink

CONFIG_FILE="src/config.ini"


if __name__ == '__main__':
    """Funkcja głowna
    """
    try:
        utils.initConfig(CONFIG_FILE)
        utils.initLogger(glob.cfg['LOG']['FileName'],consoleLogger=False)
        try:
            moduleConfig=utils.initConfigModel(glob.cfg['CONFIG_JSON']['FileName'])

            tui = TuiRoboDataLink(moduleConfig)

            ioManager = RoboDataIO(moduleConfig,tui)


            #tworzenie menadżera modułów
            #
            #ioManager.initInputsBuffer()



            
            tui.run()


            
                                
        except ValidationError as err:
            glob.log.error(err)


    except FileNotFoundError as err:
        print(err)
    except NameError as err:
        print(err)
        
        