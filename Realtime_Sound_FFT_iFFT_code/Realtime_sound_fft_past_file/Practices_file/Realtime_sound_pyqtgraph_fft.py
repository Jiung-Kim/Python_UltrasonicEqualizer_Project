# 출처 : Let's Build an Audio Spectrum Analyzer in Python! (pt. 3) Switching to PyQtGraph
# https://www.youtube.com/watch?v=RHmTgapLu4s&list=PLh8dV4ohqrFVw3ttwYrLzGfpJtX9UaNyu&index=3

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys
import pyaudio
import os
import struct
from scipy.fftpack import fft
from scipy.fftpack import ifft

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
        
        # self.canvas = self.win.addPlot(title="Pytelemetry")

        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1)
        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1)

        #pyaudio stuff
        self.FORMAT = pyaudio.paInt16
        self.RATE =   44100      # 192000      # samples per second , 96000Hz
        # self.FRE_RESOLUTION = 10            # frequency domain resolution 
        # self.CHUNK =  self.RATE // self.FRE_RESOLUTION      # samples per frame,   // 는 소수점을 버리고 정수만 취한다.
        self.CHUNK = 2205 * 2 
        self.CHANNELS = 1    
        # self.SECOND_PER_FRAME = self.CHUNK / self.RATE


        # pyaudio class instance
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format= self.FORMAT,
            channels=self.CHANNELS,
            rate= self.RATE,
            input=True,
            output=True,
            frames_per_buffer= self.CHUNK
        )
        # adjust later~
        # self.t = np.array(np.linspace(0, self.SECOND_PER_FRAME, self.CHUNK)) # len(t) = CHUNK
        # self.frequency = np.array(np.arange(0, self.RATE, 1/self.SECOND_PER_FRAME ))  # len(frequencty) = CHUNK, 

        # writter original setting 
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.f = np.linspace(0, 22050, 2205)     # 정수로 나와야 한다. 


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self,name,data_x,data_y):
        if name in self.traces:
            self.traces[name].setData(data_x,data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)  # pen is color
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, self.CHUNK, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                self.spectrum.setLogMode(x=True, y= True)
                self.spectrum.setYRange(-400, 10000,  padding=0)  # 여기에 문제가 있다. 데이터수와 맞지 않는 것 같다. 
                self.spectrum.setXRange(np.log10(20), np.log10(self.RATE / 2 ), padding=0.005)

    
    def update(self):
        
        wf_data = self.stream.read(self.CHUNK)  
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128 
        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data)


        sp_data = fft(np.array(wf_data, dtype='int8')- 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]
                         ) * 2 / (128 * self.CHUNK)
        self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
        
        
       

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()
    

if __name__ == '__main__':

    audio_app = PLot2D()
    audio_app.animation()
