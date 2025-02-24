import threading
import time

import matlab.engine
import numpy as np

class MatlabSlam(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.lidarNpArrMatlab = np.zeros(360)
        self.lidarScanCounterMatlab=0
        self.eng = matlab.engine.start_matlab()
        self.eng.cd(r'~/Nextcloud/PRz/mobileRobotNotes/python/testMatlabPython', nargout=0)

    def run(self):
        while True:
            self.parent.execBeforeMatlabAlgorythm()
            with self.parent.lockMatlab:
                # Perform calculations using self.parent.lidarNpArr
                # Store results in self.parent.lidarNpArrMatlab
                self.lidarNpArrMatlab = self.parent.lidarNpArrMatlab
                self.lidarScanCounterMatlab = self.parent.lidarScanCounterMatlab
            
            
            ranges = self.lidarNpArrMatlab.tolist()

            ranges_matlab = matlab.double(ranges)
            

            t = self.eng.testFun(ranges_matlab,1,nargout=3)
            result = {'x': 1, 'y': 2, 'beta': 3}
            
            self.parent.execAfterMatlabAlgorythm(result)