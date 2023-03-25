import robo_data_globals as glob
from time import sleep
import utils
from configModel import ModuleConfig
from threading import Thread, Event, Lock
from rplidar.pyrplidar import PyRPlidar, PyRPlidarConnectionError
import numpy as np

class LidarModule(Thread):

    def __init__(self,name,ioManager,outputSendEvent:Event):
        super().__init__()
        
        self.ioManager=ioManager
        self.name =name
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.event=ioManager.event
        self.outputSendEvent = outputSendEvent
        self.n=1


        self.port = self.config.getInputByName(self.name).port
        self.baundrate = int(self.config.getInputByName(self.name).baundrate)
        self.numInt16 =  int(self.config.getInputByName(self.name).info.numBuforBytes/2)

        glob.log.info("Thread %s create",self.name)

    
    def init(self):
        testPortVal =utils.testSerialPort(self.port, self.baundrate)
        if not testPortVal:
            self.ioManager.tui.updateStatus(self.name,"Port is close")
            return False
        
        self.lidar = PyRPlidar()
        try:
            self.lidar.connect(self.port,self.baundrate,timeout=3)
            self.lidar.get_info()
        except PyRPlidarConnectionError as err:
            self.ioManager.tui.updateStatus(self.name,"Lidar not found")
            return False

        self.ioManager.tui.updateStatus(self.name,"INIT: Lidar connected")
        return True
    


    def run(self):

        num=1
        
        while True:
            self.lock.acquire()
            
            glob.outputsBuffer[self.name] = np.zeros(self.numInt16,dtype=np.int16)

            self.lock.release()
            glob.log.info("THREAD {} SAVE {}".format(self.name,self.numInt16))
            
            
            if self.event.is_set():
                self.afterClose()
                break
            if self.outputSendEvent.is_set():
                self.afterSendByOutput()
                
            

            sleep(0.1)

    def afterClose(self):
        self.ioManager.tui.updateStatus(self.name,"STOP")

    def afterSendByOutput(self):
        self.ioManager.notify(self.name,"no. {}".format(self.n))
        self.n=self.n+1
        self.outputSendEvent.clear()


