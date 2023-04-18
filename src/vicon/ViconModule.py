import robo_data_globals as glob
import socket
from time import sleep
import utils
from configModel import ModuleConfig
from threading import Thread, Event, Lock
import numpy as np
import struct
import vicon.ViconUtils  as vi
class ViconModule(Thread):

    def __init__(self,name,ioManager,outputSendEvent:Event):
        super().__init__()
        
        self.ioManager=ioManager
        self.name =name
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.closeEvent=ioManager.closeEvent
        self.outputSendEvent = outputSendEvent


        self.remoteIp = self.config.getInputByName(self.name).remoteIp
        self.port = self.config.getInputByName(self.name).port
        self.size = int(self.config.getInputByName(self.name).size)
        self.gainRot = int(self.config.getInputByName(self.name).gainRot)
        self.msSleepTime = int(self.config.getInputByName(self.name).msSleepTime)

        self.numInt16 =  int(self.config.getInputByName(self.name).info.numBuforBytes/2)
        

        
        glob.log.info("Thread %s create",self.name)

    
    def init(self):

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
        self.socket.settimeout(1)
        self.socket.bind(("0.0.0.0",self.port))
        self.socket.sendto(b"",(str(self.remoteIp),self.port))
        try:
            data, addr = self.socket.recvfrom(self.size)
            self.viconData= vi.udpDataToViconData(data)
            if self.viconData.itemsInBlock==1:
                msg = "Track 1 obj: {}".format(self.viconData.items[0].name.replace('\x00',''))
            else:
                msg = "Track {} obj |ERROR".format(self.viconData.itemsInBlock)

            self.ioManager.tui.updateStatus(self.name,"INIT: {}".format(msg))
            self.socket.close()
        

        except socket.timeout:
            self.ioManager.tui.updateStatus(self.name,"INIT: Vicon not found")
            return False
        except ConnectionResetError:
            self.ioManager.tui.updateStatus(self.name,"INIT: Vicon not found")
            return False
        return True



    


    def run(self):
        self.lock.acquire()
        glob.outputsBuffer[self.name] = np.zeros(self.numInt16,dtype=np.int16)
        self.lock.release()
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
        self.socket.settimeout(3)
        self.socket.bind(("0.0.0.0",self.port))
        self.socket.sendto(b"",(str(self.remoteIp),self.port))
        self.errorNo=0
        while True:
            self.socket.sendto(b"",(str(self.remoteIp),self.port))
            try:
                data, addr = self.socket.recvfrom(self.size)
                self.viconData= vi.udpDataToViconData(data)
                msg = "err frame no. {}".format(self.errorNo)
                self.ioManager.tui.updateStatus(self.name,"INIT: {}".format(msg))
                sleep(0.0500)
                if self.closeEvent.is_set():
                    self.afterClose()
                    break
                if self.outputSendEvent.is_set():
                    self.afterSendByOutput()
                
            except socket.timeout:
                self.errorNo=self.errorNo+1
            #    break
            except ConnectionResetError:
                self.errorNo=self.errorNo+1
           #     break
            #
            

    def afterClose(self):
        self.socket.close()
        self.ioManager.tui.updateStatus(self.name,"STOP")

    def afterSendByOutput(self):
        if self.viconData.itemsInBlock==1:
            sendDataItem = self.viconData.items[0]
        else:
            sendDataItem = vi.PosObject()
        self.lock.acquire()
        glob.outputsBuffer[self.name] =sendDataItem.toArrayWithChecksum(self.gainRot)
        self.lock.release()
        self.outputSendEvent.clear()


