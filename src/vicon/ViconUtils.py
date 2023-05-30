import numpy as np
from struct import *
class PosObject:

    def __init__(self) -> None:
        self.name=""
        self.transX=0
        self.transY=0
        self.transZ=0
        self.rotX=0
        self.rotY=0
        self.rotZ=0

    def setName(self,name):
        self.name=name
    
    def setPoz(self,x,y,z,rotX,rotY,rotZ) -> None:
        self.transX=x
        self.transY=y
        self.transZ=z
        self.rotX=rotX
        self.rotY=rotY
        self.rotZ=rotZ

    def toArrayWithChecksum(self,rotGain):
        iTX=np.int16(self.transX)
        iTY=np.int16(self.transY)
        iTZ=np.int16(self.transZ)

        checksum = np.int16(np.round(np.double(iTX+iTY+iTZ)/3.0))
        #array size - 18 bytes
        #arrray format[TX,TY,TZ,RX*gain,RY*gain,RZ*gain,100(const),100(const),checksum]
        return np.array([self.transX,
                         self.transY,
                         self.transZ,
                         self.rotX*rotGain,
                         self.rotY*rotGain,
                         self.rotZ*rotGain,
                         100,100,
                         checksum],dtype=np.int16)
    
    def __str__(self) -> str:
        pozStr = "x: {}, y: {}, z: {}".format(self.transX,self.transY,self.transZ)
        rotStr = "rotX: {}, rotY: {}, rotZ: {}".format(self.rotX,self.rotY,self.rotZ)
        return "{} pos: {} ; rot: {}".format(self.name,pozStr,rotStr)

class ViconData:

    def __init__(self) -> None:
        self.frameNumber = 0 
        self.itemsInBlock=0
        self.items = []

    def setFrameNumber(self,fn):
        self.frameNumber=fn 

    def setItemsInBlock(self,itemsInBlock):
        self.itemsInBlock = itemsInBlock

    def addItem(self,item: PosObject):
        self.items.append(item)

def udpDataToViconData(data):

    viconData= ViconData()
    fn,itemsInBlock = unpack('ib',data[:5])
    viconData.setFrameNumber(fn)
    viconData.setItemsInBlock(itemsInBlock)
    for i in range(itemsInBlock):
        objPosData = unpack('24sdddddd',data[8+i*75:80+i*75])
        item = PosObject()
        item.setName(objPosData[0].decode("utf-8"))
        item.setPoz(objPosData[1],objPosData[2],objPosData[3],
                objPosData[4],objPosData[5],objPosData[6])
        viconData.addItem(item)
    return viconData

