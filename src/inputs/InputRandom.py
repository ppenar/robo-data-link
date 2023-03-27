import robo_data_globals as glob
from time import sleep
import utils
from configModel import ModuleConfig
from threading import Thread, Event, Lock
import numpy as np

class InputRandom(Thread):

    def __init__(self,name,ioManager,outputSendEvent:Event):
        super().__init__()
        
        self.ioManager=ioManager
        self.name =name
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.closeEvent=ioManager.closeEvent
        self.outputSendEvent = outputSendEvent
        self.n=1


        self.msSleepTime = self.config.getInputByName(self.name).msSleepTime
        self.numInt16 =  int(self.config.getInputByName(self.name).info.numBuforBytes/2)

        glob.log.info("Input thread %s create",self.name)

    
    def init(self):
        glob.log.info("Input thread %s: INIT",self.name)

        self.lock.acquire()
        self.ioManager.notify(self.name,"INIT")
        self.lock.release()
    
        return True
    


    def run(self):

        num=1
        
        while True:
            randomData=np.random.randint(100,size=self.numInt16,
                                         dtype=np.int16)
            
            self.lock.acquire()
            glob.outputsBuffer[self.name] = randomData
            self.lock.release()
            
            glob.log.info("THREAD {} SAVE {}".format(self.name,self.numInt16))
            
            
            if self.closeEvent.is_set():
                self.afterClose()
                break
            if self.outputSendEvent.is_set():
                self.afterSendByOutput()

            sleep(float(self.msSleepTime)/1000.0)

    def afterClose(self):
        self.ioManager.tui.updateStatus(self.name,"STOP")

    def afterSendByOutput(self):
        self.ioManager.notify(self.name,"no. {}".format(self.n))
        self.n=self.n+1
        self.outputSendEvent.clear()


