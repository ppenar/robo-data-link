import npyscreen
from configModel import Info
import utils 
class TuiBox:


    def __init__(self,info:Info, number, type="io",maxWidth=60) -> None:
        self.info=info
        self.number=number
        self.type = type 
        self.maxWidth=maxWidth
        if type =="io":
            self.lines = ["Name: {}".format(self.info.name),
                "Desc: {}".format(self.info.desc),
                "",
                "STATUS: unknown"]
        else:
            self.lines = utils.getInfoBoxTexList()


    def setNpyBoxRef(self,npbox: npyscreen.BoxTitle):
        self.npbox = npbox
        self.npbox.values = self.lines

    def getRelxRely(self):
        if self.number%2==0:
            return [self.maxWidth+4,2+(self.number-2)*3]
        else: 
            return [2,2+(self.number-1)*3]
        
    def setStatus(self,text):
        self.lines[3]="STATUS: {}".format(text)
        self.npbox.clear()
        self.npbox.set_value(value=self.lines)
        self.npbox.display()
