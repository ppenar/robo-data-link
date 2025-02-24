import robo_data_globals as glob
from time import sleep
import utils
from threading import Thread, Event, Lock
import numpy as np
import serial

class FileOutput(Thread):

    def __init__(self,ioManager):
        super().__init__()
        
        self.ioManager=ioManager
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.closeEvent=ioManager.closeEvent

        self.inputs = ioManager.config.getInputs()

        self.name = self.config.getOutput().info.name
        self.path = self.config.getOutput().path
        self.msSleepTime = self.config.getOutput().msSleepTime

        self.n=0
        

        glob.log.info("Output thread %s create",self.name)

    
    def init(self):

        try:
            self.file = open(self.path, 'wb')
        except IOError as e:
            glob.log.error("Failed to open file %s: %s", self.path, str(e))
            self.ioManager.notify(self.name, "Failed to open file")
            return False



        
        self.ioManager.tui.updateStatus(self.name,"INIT: File is Open")
        return True
    


    def run(self):
        self.ioManager.notify(self.name,"START | sleepTimeMs : {}".format(self.msSleepTime))
        
        while True:
            sendData = np.array([],dtype=np.int16)
         #   self.n=self.n+1
            self.lock.acquire()
            i = self.inputs[self.n]
            sendData = glob.outputsBuffer[i.info.name]

            # Convert sendData to a list of decimal strings
            decimal_data = ' '.join(map(str, sendData.tolist()))
            # Write the decimal data to the file
            self.file.write((decimal_data + '\n').encode())
            #for i in self.inputs:
            #    name = i.info.name    
            #    sendData = np.concatenate((sendData,glob.outputsBuffer[name]))
            self.lock.release()
            
            self.ioManager.setOutputSendEvent()


            if self.closeEvent.is_set():
                self.afterClose()
                break
            #sleep(float(self.msSleepTime)/1000.0)
            sleep(0.1)         

    def afterClose(self):
        self.file.close()
        self.ioManager.tui.updateStatus(self.name,"STOP")



