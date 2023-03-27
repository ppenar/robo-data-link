import robo_data_globals as glob
from time import sleep
import utils
from threading import Thread, Event, Lock
import numpy as np
import serial

class SerialOutput(Thread):

    def __init__(self,ioManager):
        super().__init__()
        
        self.ioManager=ioManager
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.closeEvent=ioManager.closeEvent

        self.inputs = ioManager.config.getInputs()

        self.name = self.config.getOutput().info.name
        self.port = self.config.getOutput().port
        self.baundrate = self.config.getOutput().baundrate
        self.msSleepTime = self.config.getOutput().msSleepTime
        

        glob.log.info("Output thread %s create",self.name)

    
    def init(self):
        testPortVal =utils.testSerialPort(self.port, self.baundrate)
        if not testPortVal:
            self.ioManager.notify(self.name,"Port is close")
            return False
        
        self.serial = serial.Serial(port=self.port,
                                    baudrate=self.baundrate,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS)
       
        if self.serial.is_open:
            self.ioManager.tui.updateStatus(self.name,"INIT: Port is Open")
        else:
            self.ioManager.tui.updateStatus(self.name,"INIT: Serial port problem") 
        return True
    


    def run(self):
        self.ioManager.notify(self.name,"START | sleepTimeMs : {}".format(self.msSleepTime))
        
        while True:
            sendData = np.array([],dtype=np.int16)
            self.lock.acquire()
            for i in self.inputs:
                name = i.info.name    
                sendData = np.concatenate((sendData,glob.outputsBuffer[name]))
            self.lock.release()
            self.serial.write(sendData.tobytes())
            self.ioManager.setOutputSendEvent()


            if self.closeEvent.is_set():
                self.afterClose()
                break
            sleep(float(self.msSleepTime)/1000.0)
                       

    def afterClose(self):
        self.serial.close()
        self.ioManager.tui.updateStatus(self.name,"STOP")



