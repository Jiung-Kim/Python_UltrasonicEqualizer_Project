# 출처 : Let's Build an Audio Spectrum Analyzer in Python! (pt. 3) Switching to PyQtGraph
# https://www.youtube.com/watch?v=RHmTgapLu4s&list=PLh8dV4ohqrFVw3ttwYrLzGfpJtX9UaNyu&index=3

# 필요한것만 적자 
# Realtime_sound_pyqtgraph_ftt_adjust.py 파일에서 시작했다. 2020.9.24 

from pyqtgraph.Qt import QtGui, QtCore 
import numpy as np
import pyqtgraph as pg
import sys
import pyaudio
import os
import struct
import matplotlib.pyplot as plt
from scipy import fftpack
import sounddevice as sd


class ultrasonic(object):
    def __init__(self, RATE = 192000 , BLOCKING_LOW_FREQUENCY = 0, BLOCKING_HIGH_FREQUENCY = 0, SHIFT_FREQUENCY = 0):
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title="basic plotting examples")   
        self.win.resize(700, 800)                              # 윈도우 창 초기 크기 
        self.win.setWindowTitle('ultrasonic_sound_equalizer')  # 윈도우 창 타이틀 
        self.win.setBackground('k')                            
        # 백그라운드 색깔 k is black, w is white and more b, g, r, c, m, y
        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1)
        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1)
        self.manipulation_spectrum = self.win.addPlot(title='Manipulated SPECTRUM', row=3, col=1)
        self.re_waveform = self.win.addPlot(title='Manipulated IFFT WAVEFORM', row=4, col=1)

        ######################pyaudio stuff##########################
        self.RATE = RATE    # 192000              
        # samples per second , 192000Hz
        self.FRE_RESOLUTION = 20       # default 20       
        # frequency domain resolution 
        self.CHUNK =  self.RATE // self.FRE_RESOLUTION      
        # samples per frame,   // 는 소수점을 버리고 정수만 취한다. 
        self.FORMAT = pyaudio.paInt16    # pyaudio.paInt16   pyaudio.paFloat32
        # audio format (bytes per sample?)
        self.CHANNELS = 1                     
        # single channel for microphone
        self.SECOND_PER_FRAME = self.CHUNK / self.RATE   
        # second per frame, 한 프레임당 걸리는 시간 
        self.BLOCKING_LOW_FREQUENCY = BLOCKING_LOW_FREQUENCY      # default 0
        # LOW range frequency blocking filter, Hz
        self.BLOCKING_HIGH_FREQUENCY = BLOCKING_HIGH_FREQUENCY    # default 0
        # HIGH range frequency blocking filter, Hz
        self.SHIFT_FREQUENCY = SHIFT_FREQUENCY                    # default 0     
        # 주파수 data를 이동시킬 주파수 
        self.mic_device = 1
        # 입력 장치 번호 
        self.speaker_device = 3 
        # 출력 장치 번호 
        ####################### pyaudio class input instance##################
        self.p = pyaudio.PyAudio()    #한번만 선언해주면 된다.
        self.stream = self.p.open(
            format= self.FORMAT,
            channels=self.CHANNELS,
            rate= self.RATE,
            input_device_index = self.mic_device,
            input = True,
            # output=True,
            frames_per_buffer= self.CHUNK
        )

        ###################### pyaudio class output instance #####################
        self.player = self.p.open(
            format= pyaudio.paInt16, 
            # pyaudio.paFloat64 는 pyaudio에서 지원 안한다. pa.Float32 까지 가능하다.
            channels=self.CHANNELS,
            rate= self.RATE,
            output_device_index = self.speaker_device,
            # input=True,
            output = True,
            frames_per_buffer= self.CHUNK
        )

        ###################linear time, frequency axis array ###################
        self.time = np.array(np.linspace(0, self.SECOND_PER_FRAME, self.CHUNK)) 
        
        self.half_time = np.array(np.linspace(0, self.SECOND_PER_FRAME, self.CHUNK//2))

        self.frequency = np.array(np.arange(0, self.RATE, 1/self.SECOND_PER_FRAME ))  

        self.half_frequency = np.array(np.arange(0, self.RATE//2, 1/(self.SECOND_PER_FRAME )) )

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='y', widthhh=10)  
                # pen is graph color
                self.waveform.setYRange(-255, 255, padding=0.0)
                self.waveform.setXRange(0, self.SECOND_PER_FRAME, padding=0.0)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='c', width=5)
                # self.spectrum.setLogMode(x=True, y= True)              
                # # 로그 스케일로 axis 표현할때 
                self.spectrum.setYRange(0, 0.25, padding=0.05)             
                self.spectrum.setXRange(0, self.RATE//2, padding=0.01)   
                
            if name == 'manipulation_spectrum':
                self.traces[name] = self.manipulation_spectrum.plot(pen='m', width=10)
                # self.manipulation_spectrum.setLogMode(x=True, y= True)        
                # # 로그 스케일로 axis 표현할때 
                self.manipulation_spectrum.setYRange(0, 0.25, padding=0.05)       
                # padding 는 axis가 시작, 끝나는 지점의 위치를 움겨준다. 
                self.manipulation_spectrum.setXRange(0, self.RATE//2, padding=0.01)   
            if name == 're_waveform':
                self.traces[name] = self.re_waveform.plot(pen='w', width=10)  # pen is color
                self.re_waveform.setYRange(-255, 255, padding=0.0)
                self.re_waveform.setXRange(0, self.SECOND_PER_FRAME, padding=0.0)

    def update(self):
        ## def update() 가 무한 루프고 마이크에서 sample 를 받아서 출력하는 것은 가능하다.  
        ############################# Waveform data  ###################################
        # sample =np.fromstring(self.stream.read(self.CHUNK ,exception_on_overflow = False),dtype=np.int16)  # 지금 이거 되거든 dtype 맞추면 되는거 같다. 

        # wf_data = self.stream.read(self.CHUNK) 
        wf_data = self.stream.read(self.CHUNK, exception_on_overflow = False)  # exception_on_overflow = False 이 말이 무었인지 모르겠다. 
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)   
        wf_data = np.array(wf_data, dtype='b')[::2]  
        # 중간 값을 0으로 한다. 

        self.set_plotdata(name='waveform', data_x=self.time, data_y=wf_data)   
        # x axis = time, y axis = wf_data updated


        ############################## FFT data  ######################################
        sp_data = fftpack.fft(np.array(wf_data, dtype='int16'))
        # sp_data = fftpack.fft(np.array(wf_data))   
        sp_data_half_abs = np.abs(sp_data[0:int(self.CHUNK)//2]) * 2 / (128 * self.CHUNK)    
        
        self.set_plotdata(name='spectrum', data_x=self.half_frequency, data_y=sp_data_half_abs)  
        # x axis = half_frequency, y axis = sp_data_half_abs   updated


        ######################## Manipulating FFT data  #############################
        m_sp_data = sp_data.copy() 
        m_sp_data[0:int(self.BLOCKING_LOW_FREQUENCY)//int(self.FRE_RESOLUTION)+1] = 0
        # cut the low frequency
        if self.BLOCKING_HIGH_FREQUENCY == 0 : 
            pass
        else : 
            m_sp_data[int(self.BLOCKING_HIGH_FREQUENCY)//int(self.FRE_RESOLUTION):] = 0
        # cut the high frequency , high fre. == 0 일땐 cut을 하지 않는다. 

        if self.SHIFT_FREQUENCY == 0 : 
            pass
        else:
            m_sp_data[int(self.RATE)//(2*int(self.FRE_RESOLUTION)):] = 0 
            # remove above shift frequency data 
            m_sp_data[int(self.SHIFT_FREQUENCY) // int(self.FRE_RESOLUTION) : (int(self.RATE)//(2*int(self.FRE_RESOLUTION))+int(self.SHIFT_FREQUENCY) // int(self.FRE_RESOLUTION) )] = m_sp_data[0: int(self.RATE)//(2*int(self.FRE_RESOLUTION))]
            # shift total frequency data
            m_sp_data[:int(self.SHIFT_FREQUENCY)//int(self.FRE_RESOLUTION)] = 0
            # remove below shift frequency data 

        m_sp_data_half_abs = np.abs(m_sp_data[:int(self.CHUNK)//2]) * 2 / (128 * self.CHUNK)    
        # absoluted m_sp_data

        self.set_plotdata(name='manipulation_spectrum', data_x=self.half_frequency, data_y=m_sp_data_half_abs)  
        # x axis = half_frequency, y axis = m_sp_data_half_abs   updated


        ######################## Manipulated IFFT WAVEFORM  #########################
        re_wp_data = fftpack.ifft(m_sp_data.copy())   # len() = 9600 is CHUNK
        re_wp_data_real = np.real(re_wp_data) * 1.0 
        self.set_plotdata(name='re_waveform', data_x=self.time, data_y=re_wp_data_real)
        # x axis = time, y axis = re_wp_data_real  updated
        
        #################### Output the Manipulated IFFT Sound #####################
        output =re_wp_data.copy()  
        # re_wp_data의 format은 np.flat64
        # output_float32 = (np.real(output) * 1.0 / 127.500).astype(np.float32)    
        # .astype( name ) 은 데이터의 타입을 name으로 바꿔준다. 
        # format이 float32 일때, float32 은 데이터 범위가 [-1~1]이다. 
        output_int16 = (np.real(output) * 32768 // 128).astype(np.int16)   
        # format이 int16 일때, int16 은 2^16 데이터 분해이므로 [ -32678 ~ 32767 ] 범위를 가져야 한다. 
        
        self.player.write(output_int16, self.CHUNK)
        # output을 스피커로 출력한다. 
        # return print(output.dtype, max(output), min(output)) 
        
        # time.sleep(1) # second 로 pause 역활을 한다. 


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        # timer.timeout.connect(self.stream_out)
        # time.sleep(10)
        timer.start(0)     
        #start(ms) animation 내의 함수 실행에 딜레이(delay)를 준다. 1000은 1000ms=1second 이다. 
        self.start()    

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    # print(sd.query_devices())
    # 음성 출력, 입력 device들의 번호를 출력한다.
    realtimesound = ultrasonic(RATE = 192000, BLOCKING_LOW_FREQUENCY = 0, BLOCKING_HIGH_FREQUENCY = 0, SHIFT_FREQUENCY = 300)  # unit Hz
    realtimesound.animation()



