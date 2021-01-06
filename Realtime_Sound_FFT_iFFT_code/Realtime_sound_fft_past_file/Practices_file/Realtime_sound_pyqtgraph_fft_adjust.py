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
        # self.phase = 0   # 필요 없음
        # self.t = np.arange(0, 3.0, 0.01) # 필요없음 
        pg.setConfigOptions(antialias=True)
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title="basic plotting examples")   
        self.win.resize(700, 600)                              # 윈도우 창 초기 크기 
        self.win.setWindowTitle('pyqtgraph example: plotting')  # 윈도우 창 타이틀 
        
        # self.canvas = self.win.addPlot(title="Pytelemetry")

        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1)
        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1)

        #pyaudio stuff
        self.RATE =  192000              # samples per second , 96000Hz
        self.FRE_RESOLUTION = 20            # frequency domain resolution 
        self.CHUNK =  self.RATE // self.FRE_RESOLUTION      # samples per frame,   // 는 소수점을 버리고 정수만 취한다. 
        self.FORMAT = pyaudio.paInt16         # audio format (bytes per sample?)
        self.CHANNELS = 1                     # single channel for microphone
        self.SECOND_PER_FRAME = self.CHUNK / self.RATE  # second per frame, 한 프레임당 걸리는 시간 
        # BLOCKING_LOW_FREQUENCY = 100     # LOW range frequency blocking filter, Hz
        # BLOCKING_HIGH_FREQUENCY = 10000  # HIGH range frequency blocking filter, Hz
        # SHIFT_FREQUENCY = 30000         # 주파수 data를 이동시킬 주파수 


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
        self.x = np.array(np.linspace(0, self.SECOND_PER_FRAME, self.CHUNK)) # len(t) = CHUNK
        self.f = np.array(np.arange(0, self.RATE, 1/self.SECOND_PER_FRAME ))  # len(frequencty) = CHUNK, 

        # writter original setting 
        # self.x = np.arange(0, 2 * self.CHUNK, 2)
        # self.f = np.linspace(0, 22050, 2205) # 정수로 나와야 한다. 


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self,name,data_x,data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)  # pen is color
                self.waveform.setYRange(-255, 255+255, padding=0)
                self.waveform.setXRange(0, self.SECOND_PER_FRAME, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                # self.spectrum.setLogMode(x=True, y= True)
                self.spectrum.setYRange(0, 2, padding=0.1)             # padding  눈금 간격을 결정한다. 
                self.spectrum.setXRange(0, self.RATE, padding=0.01)   # padding의 의미는?


    
    def update(self):
        
        wf_data = self.stream.read(self.CHUNK)  
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128 
        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data)


        sp_data = fft(np.array(wf_data, dtype='int8') - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK)]) * 2 / (128 * self.CHUNK)
        self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
        
        
       

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)     #start( ms) animation 내의 함수 실행에 딜레이(delay)를 준다. 1000은 1000ms=1second 이다. 
        self.start()    
    

if __name__ == '__main__':

    audio_app = PLot2D()
    audio_app.animation()
