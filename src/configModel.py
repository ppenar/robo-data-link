from ipaddress import IPv4Address

class Info:
    """
        Klasa reprezentuje obiekt, przypisany do parametru info w pliku konfiguracyjnym

        Parametry
        ----------
            name : str
                nazwa modułu
            desc : str
                Opis moduły wyświetlany w TUI/GUI
            implementedBy : str
                nazwa klasy, która implementuje wątek I/O, który obsługuje opisywany moduł
            numBuforBytes: int
                liczba bajtów w buforze. Bufor to tablica numpy, w której typ danych to int16, dlatego
                bufor stanowi numBuforBytes/2 liczb. 
        """
    def __init__(self,name:str,desc:str,implementedBy:str,numBuforBytes:int
                 ) -> None:
        self.name,self.desc,self.implementedBy=name,desc,implementedBy
        self.numBuforBytes=numBuforBytes

class OutputDemo:
    """
        Klasa reprezentuje demonstracyjną konfiguracje wyjścia
        
        Parametry
        ----------
            info : Info
                informacje o module
            msSleepTime: int
                czas pauzy w wątku
    """
    def __init__(self,info:Info,
                 msSleepTime:int):
        self.info=info
        self.msSleepTime = msSleepTime


class InputRandom:
    """
        Klasa reprezentuje demonstracyjną konfiguracje wejścia
        
        Parametry
        ----------
            info : Info
                informacje o module
            msSleepTime: int
                czas pauzy w wątku
    """
    def __init__(self,info:Info,
                 msSleepTime:int):
        self.info=info
        self.msSleepTime = msSleepTime


class Serial:
    """
        Klasa reprezentuje konfiguracje portu szeregowego, który będzie stanowić możliwe wyjście z aplikacji
        
        Parametry
        ----------
            info : Info
                informacje o module
            port : str
                nazwa portu szeregowego wykorzystanego do komunikacji z Dspace
            baundrate : int
                szybkość komunikacji portu szeregowego
            join: bool
                wartość określa, czy bajty stanowiące bufory różnych wejść mają być połączone jako kolejne bajty jednej ramki
            msSleepTime: int
                czas pauzy w wątku
    """
    def __init__(self,info:Info, port:str, 
                 baundrate:int, join:bool, 
                 msSleepTime:int):
        self.info=info
        self.port = port
        self.baundrate =baundrate
        self.join=join
        self.msSleepTime = msSleepTime

class Tcp:
    """
        Klasa reprezentuje konfiguracje wyjścia TCP
        
        Parametry
        ----------
            info : Info
                informacje o module
            ip : IPv4Address
                adres IP
            port : int
                port
            mode: str
                tryb działania wyjścia. Możliwe wartości to Command lub Continous
            msSleepTime: int
                czas pauzy w wątku
    """
    def __init__(self,info:Info,ip:IPv4Address,
                 port:int,mode:str,
                 msSleepTime: int) -> None:
        self.info, self.ip = info,ip
        self.port, self.mode = port,mode 
        self.msSleepTime =msSleepTime

class Lidar:
    """
        Klasa reprezentuje konfiguracje lidara, który będzie stanowić możliwe wejście 
        
        Parametry
        ----------
            info : Info
                informacje o module
            port : str
                nazwa portu szeregowego wykorzystanego do komunikacji z lidarem
            baundrate : int
                szybkość komunikacji portu szeregowego
            stepAngle: int
                krok odczytu stopni
    """
    def __init__(self,info:Info, port:str, baundrate:int,stepAngle:int) -> None:
        self.info = info
        self.port,self.baundrate =port,baundrate
        self.stepAngle = stepAngle

class Leica:
    """
        Klasa reprezentuje konfiguracje wejścia w postaci trackera laserowego Leica
        
        Parametry
        ----------
            info : Info
                informacje o module
            ip : IPv4Address
                adres IP
            port : int
                port
            mode: str
                tryb działania trackera. Możliwe wartości to Stationary,Distance lub Continous
    """
    def __init__(self,info:Info,ip:IPv4Address,
                 port:int, mode:str) -> None:
        self.info = info
        self.ip,self.port,self.mode = ip,port,mode

class ModuleConfig:
    """
        Klasa reprezentuje konfiguracje programu poprzez określenie wyjścia i jego konfiguracji oraz listy wejść oraz ich konfiguracji
        
        Parametry
        ----------
            profil : str
                nazwa konfiguracji/profilu konfiguracji
            inputs : list
                lista nazw wejść
            output : str
                nazwa wyjścia
            dspace : :class:`Despace`
                pole, którego wartość to obiekt opisujący konfiguracje karty dspace. W przypadku, gdy w danej konfiguracji nie jest używany =None
            tcp : :class:`Tcp`
                pole, którego wartość to obiekt opisujący konfiguracje wyjścia jako TCP. W przypadku, gdy w danej konfiguracji o wyjście nie jest używane =None
            lidar : :class:`Lidar`
                pole, którego wartość to obiekt opisujący konfiguracje lidara RP1. W przypadku, gdy w danej konfiguracji to wejście nie jest używane =None            
            leica : :class:`Leica`
                pole, którego wartość to obiekt opisujący konfiguracje trackera laserowego Leica. W przypadku, gdy w danej konfiguracji to wejście nie jest używane =None
        """
    def __init__(self,profil:str,inputs:list,output:str,
                 tcp:Tcp=None, serial : Serial=None,
                 lidar:Lidar=None,leica: Leica=None,
                 inputrandom1: InputRandom =None, inputrandom2: InputRandom =None):
        self.profil =profil
        self.inputs=inputs
        self.output=output
        self.tcp =tcp
        self.lidar = lidar
        self.leica = leica
        self.serial = serial


        self.inputrandom1=inputrandom1
        self.inputrandom2=inputrandom2

    def getOutput(self):
        """Zwraca obiekt opisujący konfiguracje danego wyjścia

        :return: obiekt opisujący konfiguracje wyjścia
        """
        return getattr(self,self.output); 
    
    def getInputs(self):
        """Zwraca listę obiektów konfigurujących wejścia

        :return: lista obiektów konfigurujących wejścia
        :rtype: List<ConfigObj>
        """
        list=[]
        for inputName in self.inputs:
            list.append(getattr(self,inputName))
        return list 
    
    def getInfoInputs(self):
        """Zwraca listę obiektów przypisanych do klucza info 
        obiektów konfigurujących wejścia

        :return: lista obiektów konfigurujących wejścia
        :rtype: List<Info>
        """
        list=[]
        for inputName in self.inputs:
            list.append(getattr(self,inputName).info)
        return list
    
    def getInputByName(self,inputName):
        """Zwraca konfiguracje wejścia o podanej nazwie

        :return: obiekt konfigurujący wejście
        :rtype: <InputConfig>
        """
        
        return getattr(self,inputName)