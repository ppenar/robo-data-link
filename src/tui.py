import robo_data_globals as glob
import npyscreen, curses
import tuiBox
from configModel import ModuleConfig, Info


class TuiRoboDataLink(npyscreen.NPSAppManaged):
    def __init__(self,config:ModuleConfig):
        super().__init__()
        self.config=config

    def onStart(self):
        self.form = TuiRoboDataLinkMainForm(self.config,self)
        self.registerForm("MAIN",self.form)

    def updateStatus(self,name,statusTxt):
        self.form.box[name].setStatus(statusTxt)
    
    def setObserver(self,obser):
        self.observer = obser 

    def execCommand(self,name):
        self.observer.tuiExecCommand(name)
    
    def closeApp(self):
        self.form.parentApp.switchForm(None)




class TuiRoboDataLinkMainForm(npyscreen.FormWithMenus):
    def __init__(self, config,appManager,*args, **keywords):
        super().__init__(*args, **keywords)
        self.configModel = config
        self.outputBox =None
        self.appManager=appManager


        currentMax=60
        if int(self.max_x/2)<70:
            currentMax = int(self.max_x/2)-10

        
        
        infoList=self.configModel.getInfoInputs()
        infoList.append(self.configModel.getOutput().info)
        infoList.append(Info("info","","",0))

        listBoxName=["INFO","OUTPUT","INPUT"]
        num=1
        self.box={}
        for i in infoList[::-1]:
            currentType ="io"
            if i.name=="info":
                currentType="info"
            self.box[i.name] = tuiBox.TuiBox(info=i,
                                       number=num,
                                       type=currentType,
                                       maxWidth=currentMax)
            
            if num>2:
                currentBoxName = "INPUT {}".format(num-2)
            else:
                currentBoxName = listBoxName[num-1]

            pos = self.box[i.name].getRelxRely()
            self.box[i.name].setNpyBoxRef(self.add(npyscreen.BoxTitle,
                                             name=currentBoxName,
                                             relx =pos[0],
                                             rely=pos[1],
                                             max_height=6,
                                             max_width=currentMax))
            
            num=num+1

        hotKey={"^R":self.execCommand,
                "^T":self.execCommand,
                "^A":self.execCommand,
                "^Z":self.execCommand
                }
        self.add_handlers(hotKey)

    def execCommand(self,key):
        #Return a string representation of the ASCII character c
        keyStr=curses.ascii.unctrl(key)

        if keyStr=="^R":
            self.appManager.execCommand(glob.COMMAND_RUN)
        elif keyStr=="^T":
            self.appManager.execCommand(glob.COMMAND_STOP)
        elif keyStr=="^A":
            npyscreen.notify_confirm(glob.cfg["TUI"]["ABOUT"])
        elif keyStr=="^Z":
            self.appManager.execCommand(glob.COMMAND_CLOSE)
    
    