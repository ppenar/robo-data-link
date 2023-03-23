import robo_data_globals as glob
from time import sleep
from configModel import ModuleConfig
from threading import Thread, Event, Lock


class OutputDemoModule(Thread):

    def __init__(self,ioManager):
        super().__init__()
        
        self.ioManager=ioManager
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.event=ioManager.event

        self.inputs = self.config.getInputs()
        self.name = self.config.getOutput().info.name
        self.msSleepTime = self.config.getOutput().msSleepTime
        glob.log.info("Thread %s create",self.name)


    def run(self):
        num=1
        while True:
            for input in self.inputs:
                self.lock.acquire()
                data = glob.outputsBuffer[input.info.name]
                self.lock.release()
                glob.log.info("{} SEND {} BYTES PREPARE BY {}".format(self.name,
                                                                      data.size,
                                                                      input.info.name))
                msg = "Send data no. {}".format(num)
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


