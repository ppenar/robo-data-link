import utils
from tui import TuiRoboDataLink
from configModel import ModuleConfig
import robo_data_globals as glob
from threading import Event, Lock
import numpy as np

from rplidar.LidarModule import LidarModule
from inputs.InputRandom import InputRandom
from outputModule.TcpOutput import TcpOutput

class RoboDataIO:

    def __init__(self, config:ModuleConfig,tui: TuiRoboDataLink) -> None:
        self.lock =Lock()
        self.closeEvent = Event()
        self.config=config
        self.tui = tui
        self.tui.setObserver(self)

        self.initInputsBuffer()
        self.status =glob.STATUS_UNKNOWN


    def initInputsBuffer(self):
        """Inicjuje bufory wejść na podstawie parametru numBuforBytes. Bufor przechowuje liczby całkowite 16-sto bitowe, dlatego ich liczba to numBoforBytes/2
        """
        for input in self.config.getInputs():
            name = input.info.name
            numInt16 = int( input.info.numBuforBytes/2)
            glob.outputsBuffer[name] = np.zeros(numInt16,dtype=np.int16)

    def init(self):

        self.input={}
        self.sentOutputEventForInputs={}
    

        for i in self.config.getInputs():
            inputName = i.info.name
            inputImplementedBy =i.info.implementedBy
            self.sentOutputEventForInputs[inputName] = Event()
            self.input[inputName]=globals()[inputImplementedBy](inputName,
                                                                self,
                                                                self.sentOutputEventForInputs[inputName])
            self.input[inputName].init()
            
        
        self.tui.updateStatus("info",glob.STATUS_INIT)
        outputConfig=self.config.getOutput()
        outputImplementedBy = outputConfig.info.implementedBy
        self.output = globals()[outputImplementedBy](self)
        self.output.init()
        

        
        

        self.closeEvent.clear()
        

    def start(self):
        self.tui.updateStatus("info",glob.STATUS_RUN)
        for i in self.config.getInputs():
            self.input[i.info.name].start()
        self.output.start() 

    def stop(self):
        self.closeEvent.set()
        self.tui.updateStatus("info",glob.STATUS_STOP)

    def setOutputSendEvent(self):
          for i in self.config.getInputs():
            inputName = i.info.name
            self.sentOutputEventForInputs[inputName].set()
      




    def tuiExecCommand(self,name):
        glob.log.info("Exec command: {}".format(name))

        
        if name == glob.COMMAND_RUN and self.status ==glob.STATUS_INIT:
            self.start()
            self.status=glob.STATUS_RUN

        if name == glob.COMMAND_RUN and (self.status==glob.STATUS_UNKNOWN or
                                          self.status==glob.STATUS_STOP):
            self.init()
            self.status=glob.STATUS_INIT

        if name == glob.COMMAND_STOP and self.status==glob.STATUS_RUN:
            self.status=glob.STATUS_STOP
            self.stop()
            




        
    def notify(self,moduleName,msg):
        self.tui.updateStatus(moduleName,msg)



