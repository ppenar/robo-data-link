import robo_data_globals as glob
from time import sleep
from outputModule.TcpClient import TcpClient
from threading import Thread, Event, Lock
import numpy as np
import socket
import select

class TcpOutput(Thread):

    def __init__(self,ioManager):
        super().__init__()
        
        self.ioManager=ioManager
        self.config=ioManager.config
        self.lock=ioManager.lock
        self.closeEvent=ioManager.closeEvent

        self.inputs = ioManager.config.getInputs()

        self.name = self.config.getOutput().info.name
        self.ip = self.config.getOutput().ip
        self.port = self.config.getOutput().port
        self.msSleepTime = self.config.getOutput().msSleepTime
        self.mode = self.config.getOutput().mode

        glob.log.info("Output thread %s create",self.name)

    
    def init(self):
        #lista klientów
        self.clients=[]
        
        server_address =(str(self.ip),self.port)



        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)

        self.server_socket.bind(server_address)
        self.server_socket.listen(5)

        self.sockets_to_monitor = [self.server_socket]

        self.lock.acquire()
        self.ioManager.notify(self.name,"INIT: IP {}. Serv is ready".format(server_address))
        self.lock.release()
        

        return True
    


    def run(self):
        self.ioManager.notify(self.name,"waiting for the client")
        
        while True:
            read_sockets, ww, _ = select.select(self.sockets_to_monitor, 
                                                self.sockets_to_monitor, [])
            for socket in read_sockets:
                if socket is self.server_socket:
                    newConnection, clientAddress = socket.accept()
                    self.ioManager.notify(self.name,"CLIENT: {}".format(clientAddress))
                    self.sockets_to_monitor.append(newConnection)
            for socket in ww:
            
                sendData = np.array([],dtype=np.int16)
                self.lock.acquire()
                for i in self.inputs:
                    name = i.info.name    
                    sendData = np.concatenate((sendData,glob.outputsBuffer[name]))
                self.lock.release()
                socket.sendall(sendData.tobytes())
            if len(ww)>0:    
                self.ioManager.setOutputSendEvent()


            if self.closeEvent.is_set():
                self.afterClose()
                break
            sleep(float(self.msSleepTime)/1000.0)
        #    newConnection, clientAddress = self.sock.accept()
        #    newClient = TcpClient(newConnection,
        #                          clientAddress,
        #                          self.ioManager,
        #                          self.msSleepTime)
        #    self.ioManager.notify(self.name,"Client address: {}".format(clientAddress))
        #    while True:
        #        if self.closeEvent.is_set():
        #            self.afterClose()
        #            break
        #    break
                            
                

    def afterClose(self):
        self.sockets_to_monitor.clear()
        self.ioManager.tui.updateStatus(self.name,"STOP")



