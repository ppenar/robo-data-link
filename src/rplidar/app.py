
import logging
import configparser
from threading import Lock
from LidarThread import LidarThread
from DspaceThread import DspaceThread
import serial
import utils
import SharedDataModule
from pyrplidar import PyRPlidar


CONFIG_FILE = "config.ini"

dataSendArr = 111

def initConfig():
        """Czyta plik konfiguracyjny
           Przydatne: https://docs.python.org/3/library/configparser.html
        """
        cfg=configparser.ConfigParser()
        cfg.read(CONFIG_FILE)
        if cfg.has_option('NAME','NameConfigFile')==True:
           # self.log.info("Read config file: %s",self.cfg['NAME']['NameConfigFile'])
            return cfg

        else:
            return None

def initLogger():
        """
        Inicjalizacja logów dla konsoli.
        Zapis logów w pliku odbywa się poprzez dodanie kolejnego uchwytu do logera
        (przykład: https://docs.python.org/3/library/logging.handlers.html , 
        https://www.toptal.com/python/in-depth-python-logging )
        """

        #definicja uchwytu loggera dla konsoli (wyjścia standarowego)
        #consoleLogHandler = logging.StreamHandler()    
        #formatter = logging.Formatter('[%(levelname)s] %(asctime)s : %(message)s')
        #consoleLogHandler.setFormatter(formatter)
        #consoleLogHandler.setLevel(logging.INFO)

        #definicja uchwytu do pliku 

        fileLogHandler = logging.FileHandler("logFile.log", mode='w')
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s : %(message)s')
        fileLogHandler.setFormatter(formatter)
        fileLogHandler.setLevel(logging.INFO)

        #definicja logów
        log = logging.getLogger("LogDataConnector")
        log.setLevel(logging.INFO)
        #log.addHandler(consoleLogHandler)
        log.addHandler(fileLogHandler)
        log.info("Init logger")
        return log


if __name__ == "__main__":

   
    log = initLogger()
    cfg = initConfig()

    SharedDataModule.initNumPyArray()

    
    
    if cfg != None:
        log.info("Read config file: %s",cfg['NAME']['NameConfigFile'])

        deviceList =['DSPACE','LIDAR']
        testPort = utils.testPorts(deviceList,cfg)
        if testPort:
             log.info("Test ports: OK")
             lock = Lock()

             lidar = PyRPlidar()
             lidar.connect(port=cfg['SERIAL']['PORT_LIDAR'], baudrate=cfg['SERIAL']['BAUDRATE_LIDAR'], timeout=3)
             print(lidar.get_info())




             t1 = DspaceThread(log,cfg,"DSPACE",lock)
             t2 = LidarThread(lock,lidar)



             
             listThread=[t1,t2]
             for t in listThread:
                t.start()
             for i in listThread:
                t.join()
        else:
            log.error("Test ports: ERROR")


    else:
         log.error("Config file not exists")