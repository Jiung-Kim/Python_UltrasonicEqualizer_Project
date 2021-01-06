# 출처 : Let's Build an Audio Spectrum Analyzer in Python! (pt. 3) Switching to PyQtGraph
# https://www.youtube.com/watch?v=RHmTgapLu4s&list=PLh8dV4ohqrFVw3ttwYrLzGfpJtX9UaNyu&index=3


# Realtime_sound_pyqtgraph_ftt_adjust.py 파일에서 시작했다. 2020.9.24 

# Realtime_sound_fft_1.py 에서 change 한다. 
import matplotlib.pyplot as plt
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys
import pyaudio
import os
import struct
# import scipy
# import scipy.fftpack as fftpk
# from scipy.fftpack import fft
# from scipy.fftpack import ifft

import scipy.fft                 # 이 method를 쓰자 
# import matplotlib.pyplot as plt 

# %matplotlib tk  
# to display in separate Tk window

# np.set_printoptions(threshold=sys.maxsize)  # numpy 행렬  전부 출력하기 

class PLot2D(object):
    def __init__(self):
        self.traces = dict()
        

        pg.setConfigOptions(antialias=True)
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title="basic plotting examples")   
        self.win.resize(700, 700)                               # 윈도우 창 초기 크기 
        self.win.setWindowTitle('pyqtgraph example: plotting')  # 윈도우 창 타이틀 
        
        # self.canvas = self.win.addPlot(title="Pytelemetry")

        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1)
        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1)
        self.ifftwaveform = self.win.addPlot(title='Manipulated IFFT WAVEFORM', row=3, col=1)



        #pyaudio stuff
        self.RATE =  192000              # samples per second , 96000Hz
        self.FRE_RESOLUTION = 20            # frequency domain resolution 
        self.CHUNK =  self.RATE // self.FRE_RESOLUTION      # samples per frame,   // 는 소수점을 버리고 정수만 취한다. 
        self.FORMAT = pyaudio.paInt16         # audio format (bytes per sample?)
        self.CHANNELS = 1                     # single channel for microphone
        self.SECOND_PER_FRAME = self.CHUNK / self.RATE  # second per frame, 한 프레임당 걸리는 시간 
        self.BLOCKING_LOW_FREQUENCY = 10    # LOW range frequency blocking filter, Hz
        self.BLOCKING_HIGH_FREQUENCY = 29900  # HIGH range frequency blocking filter, Hz
        self.SHIFT_FREQUENCY = 30000        # 주파수 data를 이동시킬 주파수 


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
        # self.f = np.array(np.arange(0, self.RATE, 1/self.SECOND_PER_FRAME ))  # len(frequencty) = CHUNK,  
        self.f = np.array(np.arange(0, self.RATE//2, 1//(2*self.SECOND_PER_FRAME )))  # len(frequencty) = CHUNK, 길이를 절반으로 줄인다. 이유는 symetry 로 동일하기 때문에 

        # writter original setting 
        # self.x = np.arange(0, 2 * self.CHUNK, 2)
        # self.f = np.linspace(0, 22050, 2205) # 정수로 나와야 한다. 
    



















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
                # self.spectrum.setLogMode(x=True, y= True)            # 로그 스케일로 axis 표현할때 
                self.spectrum.setYRange(0, 2, padding=0.1)             # padding  눈금 간격을 결정한다. 
                self.spectrum.setXRange(0, self.RATE, padding=0.01)   # padding의 의미는?
            if name == 'ifftwaveform':
                self.traces[name] = self.ifftwaveform.plot(pen='c', width=3)  # pen is color
                # self.ifftwaveform.setYRange(0, 0.0002, padding=0)  # 범위를 아직 알수 없다.
                self.ifftwaveform.setXRange(0, self.SECOND_PER_FRAME, padding=0.005)


    
    def update(self):
        ### Waveform data
        wf_data = self.stream.read(self.CHUNK)  
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128 

        # self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data)   # pyqtgraph에 업데이트


        ### FFT data  
        sp_data = scipy.fft(np.array(wf_data, dtype='int8') - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK)//2]) * 2 / (128 * self.CHUNK)    #[0:CHUNK] 하든 안하든 sp_data 길이는 CHUNK 인것 같은데 
        sp_data =  np.abs(sp_data) * 2 / (128 * self.CHUNK)
        

        # self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)  # pyqtgraph에 업데이트

        

        ### FFT data manipulation - cut the low and high frequency 
        # sp_data[0:self.BLOCKING_LOW_FREQUENCY // self.FRE_RESOLUTION + 1] = 0   # 0hz~ BLOCKING_LOW_FREQUENCY Hz 까지 0으로 만든다. 
        # sp_data[self.BLOCKING_HIGH_FREQUENCY // self.FRE_RESOLUTION:] = 0    # BLOCKING_HIGH_FREQUENCY Hz ~ 끝까지 0으로 만든다. 
        # # FFT data manipulation - shift total frequency data 
        # sp_data[(self.SHIFT_FREQUENCY // self.FRE_RESOLUTION) : (self.SHIFT_FREQUENCY // self.FRE_RESOLUTION + self.BLOCKING_HIGH_FREQUENCY // self.FRE_RESOLUTION)] = sp_data[0:self.BLOCKING_HIGH_FREQUENCY // self.FRE_RESOLUTION ] #  0 ~ HIHG_FRE.까지의 fft 데이터를 SHIFT_FRE. ~ SHIFT_FRE.+HIHG_FRE.로 복사함. 
        # # remove the original fft data(0 ~ BLOCKING_HIGH_FREQUENCY Area) 
        # sp_data[0:self.BLOCKING_HIGH_FREQUENCY // self.FRE_RESOLUTION ] = 0 

        # self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)  # pyqtgraph에 업데이트
        
        ### Make IFFT data 
        # compute IFFT and update line
        # ifft_sp_data = np.abs(ifft(sp_data)) 
        
        # self.set_plotdata(name='ifftwaveform', data_x=self.f, data_y=sp_data)   # pyqtgraph에 업데이트


        

        return sp_data
    
    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)     #start( ms) animation 내의 함수 실행에 딜레이(delay)를 준다. 1000은 1000ms=1second 이다. 
        self.start()    

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

if __name__ == '__main__':
    
    tt = PLot2D()
    tt.animation()

    print(len(tt.update()), None//21)
    '''
    wf_data 길이는 CHUNK
    
    '''
