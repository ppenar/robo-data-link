import robo_data_globals as glob
from time import sleep
import utils
from configModel import ModuleConfig
from threading import Thread, Event, Lock
from rplidar.pyrplidar import PyRPlidar, PyRPlidarConnectionError
import numpy as np


from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel





MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 10



class LidarModule(Thread):

    def __init__(self,name,ioManager,outputSendEvent:Event):
        super().__init__()
        
        self.ioManager=ioManager
        self.name =name
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.closeEvent=ioManager.closeEvent
        self.outputSendEvent = outputSendEvent
        self.n=1


        self.port = self.config.getInputByName(self.name).port
        self.baundrate = int(self.config.getInputByName(self.name).baundrate)
        self.numInt16 =  int(self.config.getInputByName(self.name).info.numBuforBytes/2)
        self.stepAngle =  int(self.config.getInputByName(self.name).stepAngle)
        self.posInterval =  int(self.config.getInputByName(self.name).posInterval)

        self.lidarNpArr = np.zeros(360)
        self.sendData = np.zeros(self.numInt16,dtype=np.int16)
    
        self.sendArrayIndex=0

        self.currentPosInterval = 0

        self.slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

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
        self.lock.acquire()
        glob.outputsBuffer[self.name] = np.zeros(self.numInt16,dtype=np.int16)
        self.lock.release()



        
        while True:
            scan_generator = self.lidar.start_scan()
            for scan in scan_generator():


                
                angleIndex = np.rint(scan.angle).astype(np.int16)
                if angleIndex==360:
                     angleIndex=0

                
                self.lidarNpArr[359-angleIndex]=scan.distance
                    
                if self.closeEvent.is_set():
                    self.afterClose()
                    break
                if self.outputSendEvent.is_set():
                    self.afterSendByOutput()
            break
            

    def afterClose(self):
        self.lidar.stop()
        self.lidar.disconnect()
        self.ioManager.tui.updateStatus(self.name,"STOP")

    def afterSendByOutput(self):

        if self.currentPosInterval == self.posInterval and np.all(self.lidarNpArr!=0):
            self.slam.update(self.lidarNpArr,np.array(range(0,360,1)))
            x,y,theta = self.slam.getpos()
            self.sendData[0]=25
            self.sendData[1]=x
            self.sendData[2]=y
            self.sendData[3]=theta

            for i in range(4,self.numInt16-1):\
                self.sendData[i]=100
            self.sendData[self.numInt16-1]=(self.posX+self.posY)/2

            self.currentPosInterval=0

        else:
            sum = np.double(0)
            self.sendData[0]=15
            self.sendData[1]=self.sendArrayIndex
            for i in range(2,self.numInt16-1):
                d=self.lidarNpArr[self.sendArrayIndex]
                self.sendData[i]=d
                sum = sum+d
                self.sendArrayIndex=self.sendArrayIndex+self.stepAngle
                if self.sendArrayIndex>=360:
                    self.sendArrayIndex=0    
            self.sendData[self.numInt16-1] = np.round((sum+100.0)/np.double(self.numInt16-2))
            self.currentPosInterval+=1        
        
        self.lock.acquire()
        glob.outputsBuffer[self.name] = self.sendData
        self.lock.release()

        self.outputSendEvent.clear()


