import robo_data_globals as glob
from time import sleep
from rplidar.MatlabSlam import MatlabSlam
import utils
from configModel import ModuleConfig
from threading import Thread, Event, Lock
from rplidar.pyrplidar import PyRPlidar, PyRPlidarConnectionError
import numpy as np
import random

class SimLidarSlamModule(Thread):


    def __init__(self,name,ioManager,outputSendEvent:Event):
        super().__init__()
        
        self.ioManager=ioManager
        self.name =name
        self.config=ioManager.config
        self.lock=ioManager.lock

        self.lockMatlab = Lock()

        self.closeEvent=ioManager.closeEvent
        self.outputSendEvent = outputSendEvent
        self.n=1


        self.port = self.config.getInputByName(self.name).port
        self.baundrate = int(self.config.getInputByName(self.name).baundrate)
        self.numInt16 =  int(self.config.getInputByName(self.name).info.numBuforBytes/2)
        self.stepAngle =  int(self.config.getInputByName(self.name).stepAngle)

        self.lidarNpArr = np.zeros(360)
        self.lidarNpArrMatlab = np.zeros(360)

        self.lidarScanCounter=0
        self.lidarScanCounterMatlab=0

        self.matlabResult={}
        self.isMatlabResultReady=False



        self.sendData = np.zeros(self.numInt16,dtype=np.int16)
        self.sendArrayIndex=0
        glob.log.info("Thread %s create",self.name)

    
    def init(self):
        
        
        
        self.matlabThread = MatlabSlam(self)
        

        self.ioManager.tui.updateStatus(self.name,"INIT: Sim Lidar connected")
        return True
    


    def run(self):
        self.lock.acquire()
        glob.outputsBuffer[self.name] = np.zeros(self.numInt16,dtype=np.int16)
        self.lock.release()
        self.matlabThread.start()
        while True:
            ranges = [random.uniform(50, 70) for _ in range(50)]
            angles = [random.uniform(0, 360) for _ in range(50)]
            angles = [int(angle) for angle in angles]

            for i in range(50):

                self.lidarNpArr[angles[i]]=ranges[i]
                self.lidarScanCounter+=1
                    
            if self.closeEvent.is_set():
                self.afterClose()
                break
            if self.outputSendEvent.is_set():
                self.afterSendByOutput()
        
            

    def afterClose(self):
        
        self.ioManager.tui.updateStatus(self.name,"STOP")
        self.matlabThread.join()

    def afterSendByOutput(self):

        if self.isMatlabResultReady:
            self.isMatlabResultReady = False
            self.sendData[0]=1000
            self.sendData[1]=self.matlabResult['x']
            self.sendData[2]=self.matlabResult['y']
            self.sendData[3]=self.matlabResult['beta']
            for i in range(4, self.numInt16):
                self.sendData[i] = 1000
        else:
            sum = np.double(0)
            self.sendData[0] = self.sendArrayIndex

            for i in range(1, self.numInt16 - 1):
                d = self.lidarNpArr[self.sendArrayIndex]
                self.sendData[i] = d
                sum = sum + d
                self.sendArrayIndex = self.sendArrayIndex + self.stepAngle
                if self.sendArrayIndex >= 360:
                    self.sendArrayIndex = 0

            self.sendData[self.numInt16 - 1] = np.round((sum + 100.0) / np.double(self.numInt16 - 2))
        
        
        
        self.lock.acquire()
        glob.outputsBuffer[self.name] = self.sendData
        self.lock.release()

        self.outputSendEvent.clear()

    def execBeforeMatlabAlgorythm(self):
        self.lockMatlab.acquire()
        self.lidarNpArrMatlab = np.copy(self.lidarNpArr)
        self.lidarScanCounterMatlab=self.lidarScanCounter
        self.lockMatlab.release()

    def execAfterMatlabAlgorythm(self,result):
        self.isMatlabResultReady=True
        self.matlabResult=result


