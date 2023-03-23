"""
Plik z funkcjami pomocniczymi
"""

import configparser
import logging
import robo_data_globals as glob
from configModel import  ModuleConfig

import numpy as np

def initConfig(fileName):
 
    """Czyta plik konfiguracyjny. Możliwe wystąpienie dwóch wyjątków: 
        FileNotFoundError w przypadku braku pliku/nieprawidłowej ścieżki;
        NameError w przypadku braku/nieprawidłowego klucza NameConfigFile w sekcji NAME
        Przydatne: https://docs.python.org/3/library/configparser.html      

    :param fileName: nazwa pliku konfiguracyjnego
    :type fileName: String
    :return: zwraca obiekt ConfigParser jeśli plik istnieje i posiada klucz 
        NameConfigFile w sekcji NAME; inaczej zwraca None

    """
          
       
    glob.cfg=configparser.ConfigParser()
    fileList=glob.cfg.read(fileName)
    if len(fileList)<1:
        raise FileNotFoundError("ERROR: Config file not found")

    if glob.cfg.has_option('NAME','NameConfigFile')==True:
        return glob.cfg

    else:
        raise NameError("ERROR: NameConfigFile key in NAME section not exist")
   


         
        

def initLogger(logFileName='logger.log', consoleLogger=False):
        """
        Inicjalizacja logów. Zdefiniowano uchwyty loggera  i dla pliku. Logger dla konsoli jest domyślnie
        nieaktywny. Gdy nazwa pliku nie została podana, utworzony plik przyjmie nazwę logger.log
        Przydatne: https://docs.python.org/3/library/logging.handlers.html , 
        https://www.toptal.com/python/in-depth-python-logging )

        :param logFileName: nazwa tworzonego dziennika zdarzeń
        :type fileName: String

        :return: Zwraca obiekt loggera z uchwytami
        """
        if consoleLogger:
           #definicja uchwytu loggera dla konsoli (wyjścia standarowego)
           consoleLogHandler = logging.StreamHandler()    
           formatter = logging.Formatter('[%(levelname)s] %(asctime)s : %(message)s')
           consoleLogHandler.setFormatter(formatter)
           consoleLogHandler.setLevel(logging.INFO)

        #definicja uchwytu do pliku 
        fileLogHandler = logging.FileHandler(logFileName, mode='w')
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s : %(message)s')
        fileLogHandler.setFormatter(formatter)
        fileLogHandler.setLevel(logging.INFO)

        #definicja logów
        glob.log = logging.getLogger("LogDataConnector")
        glob.log.setLevel(logging.INFO)
        if consoleLogger:
            glob.log.addHandler(consoleLogHandler)
        glob.log.addHandler(fileLogHandler)
        glob.log.info("Init logger")
        return glob.log

def initConfigModel(jsonFileName):
    """Walidacja i deserializacja obiektu konfiguracyjnego z pliku JSON
    za pomocą biblioteki https://marshmallow.readthedocs.io/en/stable/
    Funkcja może zwracać wyjątek ValidationError.

    :param jsonFileName: nazwa pliku konfiguracyjnego
    :type jsonFileName: string

    :return: zwraca konfiguracje I/O wynikającą z pliku JSON
    :rtype: ModuleConfig
    """
    from json_config_scheme import JsonConfigScheme
    scheme = JsonConfigScheme()
    moduleConfigJSON = open(jsonFileName)
    jsonStr=moduleConfigJSON.read()
    moduleConfig = scheme.loads(jsonStr)
    glob.log.info("Init config model")
    return moduleConfig

def getErrorMsg(name):
    """Zwraca opis błędu zawarty w pliku konfiguracyjnym na podstawie jego nazwy. 
    Jeśli plik nie został znaleziony, zwracany jest wyjątek FileNotFoundError.

    :param name: nazwa błędu 
    :type name: string
    :raises FileNotFoundError: Jeśli nie znaleziono pliku konfiguracyjnego
    :return: Komunikat przypisany do nazwy błędu lub komunikat domyślny
    :rtype: string
    """
    c = glob.cfg
    if glob.cfg==None:
         return "Error {} message not  implemented yet".format(name)
    if glob.cfg.has_option("ERROR",name)==True:
        return glob.cfg["ERROR"][name]
    else:
        return "Error {} message not  implemented yet".format(name)

def getLeicaModeList():
    """Funkcja zwraca listę trybów działania trackera laserowego Leica.
    Lista jest tworzona na podstawie wartości klucza LeicaModeList w pliku config.ini

    :return: Lista trybów trackera Leica
    :rtype: List<Str>
    """
    #zabezpieczenia dla dokumentacji
    if glob.cfg==None:
        return []
    if glob.cfg.has_option("LEICA","LeicaModeList"):
        listModeStr = str(glob.cfg["LEICA"]["LeicaModeList"]).strip()
        listModeStr = listModeStr.replace('[','').replace(']','')
        return listModeStr.split(",")
    else:
        return []

def getTcpModeList():
    """Funkcja zwraca listę trybów działania modułu wyjścia realizowanego jako serwer TCP.
    Lista jest tworzona na podstawie wartości klucza TcpModeList w pliku config.ini

    :return: Lista trybów wyjścia TCP
    :rtype: List<Str>
    """
    #zabezpieczenia dla dokumentacji
    if glob.cfg==None:
        return []
    if glob.cfg.has_option("TCP","TcpModeList"):
        listModeStr = str(glob.cfg["TCP"]["TcpModeList"]).strip()
        listModeStr = listModeStr.replace('[','').replace(']','')
        return listModeStr.split(",")
    else:
        return []

def getInfoBoxTexList():
    """Funkcja zwraca listę stringów tworzących zawartość BOXa informacyjnego
     w TUI. Lista jest tworzona na podstawie wartości klucza InfoBoxTxt w pliku config.ini

    :return: Lista trybów wyjścia TCP
    :rtype: List<Str>
    """
    #zabezpieczenia dla dokumentacji
    if glob.cfg==None:
        return []
    if glob.cfg.has_option("TUI","InfoBoxTxt"):
        listModeStr = str(glob.cfg["TUI"]["InfoBoxTxt"]).strip()
        listModeStr = listModeStr.replace('[','').replace(']','')
        return listModeStr.split(",")
    else:
        return []