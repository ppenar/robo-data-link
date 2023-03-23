import robo_data_globals as glob
from time import sleep
from configModel import ModuleConfig
from threading import Thread, Event, Lock
import numpy as np

class InputDemoModule(Thread):

    def __init__(self,name,ioManager):
        super().__init__()
        
        self.ioManager=ioManager
        self.name =name
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.event=ioManager.event


        self.msSleepTime = self.config.getInputByName(self.name).msSleepTime
        self.numInt16 = int(self.config.getInputByName(self.name).info.numBuforBytes/2)
        glob.log.info("Thread %s create",self.name)


    def run(self):
        num=1
        
        while True:
            self.lock.acquire()
            
            glob.outputsBuffer[self.name] = np.zeros(self.numInt16,dtype=np.int16)

            self.lock.release()
            glob.log.info("THREAD {} SAVE {}".format(self.name,self.numInt16))
            msg = "Thread {} data no. {}".format(self.name,num)
            
            self.lock.acquire()
            self.ioManager.notify(self.name,msg)
            self.lock.release()
            num=num+1
            
            if self.event.is_set():
                self.afterClose()
                break
            sleep(float(self.msSleepTime)/1000.0)

    def afterClose(self):
        self.ioManager.tui.updateStatus(self.name,"STOP")
    def init(self):
        self.ioManager.tui.updateStatus(self.name,"INIT: OK")


