# 출처 : Let's Build an Audio Spectrum Analyzer in Python! (pt. 3) Switching to PyQtGraph
# https://www.youtube.com/watch?v=RHmTgapLu4s&list=PLh8dV4ohqrFVw3ttwYrLzGfpJtX9UaNyu&index=3

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys

class PLot2D(object):
    def __init__(self):
        self.traces = dict()

        self.phase = 0
        self.t = np.arange(0, 3.0, 0.01)
        
        pg.setConfigOptions(antialias=True)
        
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title="basic plotting examples")
        self.win.resize(1000, 600)
        self.win.setWindowTitle('pyqtgraph example: plotting')
        self.canvas = self.win.addPlot(title="Pytelemetry")
    
    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def trace(self,name,dataset_x,dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x,dataset_y)
        else:
            self.traces[name] = self.canvas.plot(pen='y')
    
    def update(self):
        s = np.sin(2 * np.pi * self.t +self.phase)
        c = np.cos(2 * np.pi *self.t + self.phase)

        self.trace("sin", self.t, s)
        self.trace("cos", self.t, c)
        self.phase += 0.1

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        self.start()
    

if __name__== '__main__':
    p = PLot2D()
    p.animation()