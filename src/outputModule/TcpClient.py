

from asyncio.log import logger
from cmath import log
import logging
from socket import socket
import time
import numpy as np
import robo_data_globals as glob


class TcpClient:
    """Klasa implementuje socket dla klienta. 
    Metoda clientLoop działa jako kolejny wątek programu
    """
    def __init__(self,_conn:socket,_addr,ioManager,msSleepTime) -> None:
        """Konstruktor

        :param _conn: socket klienta
        :type _conn: socket
        :param _addr: (IP,PORT) dla klienta
        :type _addr: tuple
        :param _serv: instancja serwera
        :type _serv: LeicaTCPServer
        """
        self.sock = _conn
        self.clientAddress = _addr
        self.ioManager=ioManager
        self.inputs = self.ioManager.config.getInputs()
        self.msSleepTime = msSleepTime
        self.lock=ioManager.lock
        self.closeEvent = self.ioManager.closeEvent

    def clientLoop(self):
        # nie zaimplementowano trybu command. Tu przydatne mogą być fragmenty kodu 
        # z leicaConnector:
        # msg=self.sock.recv(1024)
        #    ii = len(msg)
        #    if len(msg)==0:
                #jeśli klient się rozłączył
        #        break
        #    self.serv.app.log.info("LeicaTCPServerClient: Client %s send data",str(self.clientAddress))
        #    frame = bytesToLeicaFrame(msg)
        #    self.serv.leicaFrameRecived(self,frame)
      
      
      #  def bytesToLeicaFrame(msg):

      #        try:
      #          dataTuple= struct.unpack("llll",msg)
      #            frame = LeicaFrame(dataTuple[0],dataTuple[1],dataTuple[2],dataTuple[3])
     #       return frame
     #     except:
     #       frame = LeicaFrame(-1,-1,-1,-1)
     #       return frame
        
        
        
        while True:
            sendData = np.array([],dtype=np.int16)
            self.lock.acquire()
            for i in self.inputs:
                name = i.info.name    
                sendData = np.concatenate((sendData,glob.outputsBuffer[name]))
                self.lock.release()
            self.sock.sendall(sendData.tobytes())
            self.ioManager.setOutputSendEvent()
            if self.closeEvent.is_set():
                self.afterClose()
                break



            time.sleep(float(self.msSleepTime)/1000.0)
  
  
  
  
  
  
    def afterClose(self):
        self.sock.close()