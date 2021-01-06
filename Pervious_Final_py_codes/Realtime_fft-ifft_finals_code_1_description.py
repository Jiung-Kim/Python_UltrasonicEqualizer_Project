# 출처 : Let's Build an Audio Spectrum Analyzer in Python! (pt. 3) Switching to PyQtGraph
# https://www.youtube.com/watch?v=RHmTgapLu4s&list=PLh8dV4ohqrFVw3ttwYrLzGfpJtX9UaNyu&index=3

# 필요한것만 적자 
# Realtime_sound_pyqtgraph_ftt_adjust.py 파일에서 시작했다. 2020.9.24 

# Reference 
'''
https://www.learnpyqt.com/courses/graphics-plotting/plotting-pyqtgraph/
Qt그래프의 설정법

https://kongdols-room.tistory.com/53
https://rfriend.tistory.com/285
https://stackoverflow.com/questions/55474025/how-to-convert-int32-numpy-array-into-int16-numpy-array
numpy int, float 변환, 설정법

https://classes.engineering.wustl.edu/ese205/core/index.php?title=Audio_Input_and_Output_from_USB_Microphone_%2B_Raspberry_Pi
Audio Input and Output from USB Microphone + Raspberry Pi 

https://stackoverflow.com/questions/10733903/pyaudio-input-overflowed
wf_data = self.stream.read(self.CHUNK, exception_on_overflow = False)  
# exception_on_overflow = False 의 설명이다. 실시간 처리때는 False가 맞다. 

https://stackoverflow.com/questions/32838279/getting-list-of-audio-input-devices-in-python
audio device 찾기 코드

https://www.learnpyqt.com/courses/graphics-plotting/plotting-pyqtgraph/
pyqtgraph의 전반적인 내용 

등등 
'''

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
    def __init__(self, RATE = 192000 , BLOCKING_LOW_FREQUENCY = 0, BLOCKING_HIGH_FREQUENCY = 0, SHIFT_FREQUENCY = 0, OUTPUT_ADD_SINEWAVE = False, SINE_WAVE_VOLUME = 0.65):
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title="basic plotting examples")   
        self.win.resize(800, 700)                              # 윈도우 창 초기 크기 
        self.win.setWindowTitle('ultrasonic_sound_equalizer')  # 윈도우 창 타이틀 
        self.win.setBackground('k')                       
        # 백그라운드 색깔 k is black, w is white and more b, g, r, c, m, y
        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1)
        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1)
        self.manipulation_spectrum = self.win.addPlot(title='Manipulated SPECTRUM', row=3, col=1)
        self.add_sinewave_spectrum = self.win.addPlot(title='Manipulated and Add SineWave SPECTRUM', row=4, col=1)
        self.re_waveform = self.win.addPlot(title='Manipulated IFFT and SineWave WAVEFORM', row=5, col=1)
        


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
        self.speaker_device = 3   # 믹서 쓸땐 4
        # 출력 장치 번호 
        self.OUTPUT_ADD_SINEWAVE = OUTPUT_ADD_SINEWAVE
        # Sine Wave Volume 
        self.SINE_WAVE_VOLUME = SINE_WAVE_VOLUME
        # volume range = 1 ~ 0 , default 0.65
        ####################### pyaudio class input instance##################
        self.p = pyaudio.PyAudio()    #한번만 선언해주면 된다.
        self.stream = self.p.open(
            format= self.FORMAT,
            channels=self.CHANNELS,
            rate= self.RATE,
            input = True,
            input_device_index = self.mic_device,
            # output=True,
            frames_per_buffer= self.CHUNK
        )

        ###################### pyaudio class output instance #####################
        self.player = self.p.open(
            format= pyaudio.paInt16, 
            # pyaudio.paFloat64 는 pyaudio에서 지원 안한다. pa.Float32 까지 가능하다.
            channels=self.CHANNELS,
            rate= self.RATE,
            # input=True,
            output = True,
            output_device_index = self.speaker_device,
            frames_per_buffer= self.CHUNK
        )

        ###################linear time, frequency axis array ###################
        self.time = np.array(np.linspace(0, self.SECOND_PER_FRAME, self.CHUNK)) 
        self.frequency = np.array(np.arange(0, self.RATE, 1/self.SECOND_PER_FRAME ))  
        self.half_frequency = np.array(np.arange(0, self.RATE//2, 1/(self.SECOND_PER_FRAME )) )


        ##################### Find the audio Devices info ######################
        # for i in range(self.p.get_device_count()):
        #     print(self.p.get_device_info_by_index(i))
        #     print(self.p.get_device_info_by_index(i).get('name'))
        #     print(self.p.get_device_info_by_index(i).get('index'))
        
        # print(sd.query_devices())
        # 음성 출력, 입력 device들의 번호를 출력한다.
        

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                # waveform_pen = pg.mkPen(color=(255,0,0), width=5)
                # waveform_pen = pg.mkPen(color='y', width=1.5)
                self.traces[name] = self.waveform.plot(pen='y') 
                # self.traces[name] = self.waveform.plot(pen='y', width=1) 
                # pen is graph color,
                self.waveform.setYRange(-255, 255, padding=0.0)
                self.waveform.setXRange(0, self.SECOND_PER_FRAME, padding=0.02)
                self.waveform.setLabel('left', "Amplitude",)   
                # Axis label의 위치와 이름을 모두 정해줘야 한다. units는 
                self.waveform.setLabel('bottom', "Time", units='s') 
                # Axis label의 위치와 이름을 모두 정해줘야 한다. units의 s는 second의 s 인것같다.
            if name == 'spectrum':
                # spectrum_pen = pg.mkPen(color='c', width=1.5)
                self.traces[name] = self.spectrum.plot(pen='c')
                # self.spectrum.setLogMode(x=True, y=True)
                # self.spectrum.setYRange(-4, 0, padding=0)
                # self.spectrum.setXRange(
                #     np.log10(20), np.log10(self.RATE / 2), padding=0.005)
                # self.spectrum.setLogMode(x=True, y=False)              
                # self.spectrum.setXRange(np.log10(10), np.log10(self.RATE), padding=0.01)     
                # self.spectrum.setYRange(0, 0.4, padding=0.05)  
                # # 로그 스케일로 axis 표현할때 
                self.spectrum.setYRange(0, 0.4, padding=0.05)             
                self.spectrum.setXRange(0, self.RATE//4, padding=0.01)   
                self.spectrum.setLabel('left', "Amplitude",)   
                # Axis label의 위치와 이름을 모두 정해줘야 한다.  
                self.spectrum.setLabel('bottom', "Frequency", units='Hz') 
            if name == 'manipulation_spectrum':
                # manipulation_spectrum_pen = pg.mkPen(color='m', width=1.5)
                self.traces[name] = self.manipulation_spectrum.plot(pen='m')
                # self.manipulation_spectrum.setLogMode(x=True, y= True)        
                # # 로그 스케일로 axis 표현할때 
                self.manipulation_spectrum.setYRange(0, 0.4, padding=0.05)       
                # padding 는 axis가 시작, 끝나는 지점의 위치를 움겨준다. 
                self.manipulation_spectrum.setXRange(0, self.RATE//4, padding=0.01)   
                self.manipulation_spectrum.setLabel('left', "Amplitude",)   
                # Axis label의 위치와 이름을 모두 정해줘야 한다. units 은 label(units) 이다.
                self.manipulation_spectrum.setLabel('bottom', "Frequency", units='Hz') 
            if name == 'add_sinewave_spectrum':
                # add_sinewave_spectrum_pen = pg.mkPen(color='g', width=1.5)
                self.traces[name] = self.add_sinewave_spectrum.plot(pen='g')
                # self.manipulation_spectrum.setLogMode(x=True, y= True)        
                # # 로그 스케일로 axis 표현할때 
                self.add_sinewave_spectrum.setYRange(0, 0.4, padding=0.05)       
                # padding 는 axis가 시작, 끝나는 지점의 위치를 움겨준다. 
                self.add_sinewave_spectrum.setXRange(0, self.RATE//4, padding=0.01)   
                self.add_sinewave_spectrum.setLabel('left', "Amplitude",)   
                # Axis label의 위치와 이름을 모두 정해줘야 한다. units 은 label(units) 이다.
                self.add_sinewave_spectrum.setLabel('bottom', "Frequency", units='Hz') 
            if name == 're_waveform':
                # re_waveform_pen = pg.mkPen(color='w', width=1.5)
                self.traces[name] = self.re_waveform.plot(pen='w')  # pen is color
                self.re_waveform.setYRange(-255, 255, padding=0.0)
                self.re_waveform.setXRange(0, self.SECOND_PER_FRAME, padding=0.02)
                self.re_waveform.setLabel('left', "Amplitude",)   
                # Axis label의 위치와 이름을 모두 정해줘야 한다.  
                self.re_waveform.setLabel('bottom', "Time", units='s') 

    def update(self):
        ############################# Waveform data  ###################################
        # wf_data = self.stream.read(self.CHUNK) 
        wf_data = self.stream.read(self.CHUNK, exception_on_overflow = False)  # exception_on_overflow = False 이 말이 무었인지 모르겠다. 
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)   
        wf_data = np.array(wf_data, dtype='b')[::2]  
        # 중간 값을 0으로 한다. 

        ########################## Display to waveform update ##########################
        self.set_plotdata(name='waveform', data_x=self.time, data_y=wf_data)   
        # x axis = time, y axis = wf_data updated

        ############################## FFT data  ######################################
        # sp_data = fftpack.fft(np.array(wf_data, dtype='int16'))
        sp_data = fftpack.fft(np.array(wf_data))   
        sp_data_half_abs = np.abs(sp_data[0:int(self.CHUNK)//2]) * 2 / (128 * self.CHUNK)    

        ########################## Display to spectrum update ##########################
        self.set_plotdata(name='spectrum', data_x=self.half_frequency, data_y=sp_data_half_abs)  
        # x axis = half_frequency, y axis = sp_data_half_abs   updated

        ############################# Manipulating FFT data  #############################
        m_sp_data = sp_data.copy() 
        if self.BLOCKING_LOW_FREQUENCY == 0:  
            pass
            # Blocking low fre. = 0 이면 그냥 통과 
        else:
            m_sp_data[0:int(self.BLOCKING_LOW_FREQUENCY)//int(self.FRE_RESOLUTION)+1] = 0
            # cut the low frequency 

        if self.BLOCKING_HIGH_FREQUENCY == 0 : 
            pass
            # Blocking high fre. = 0 이면 그냥 통과 
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

        ################# Display to manipulation_spectrum update ###################
        self.set_plotdata(name='manipulation_spectrum', data_x=self.half_frequency, data_y=m_sp_data_half_abs)  
        # x axis = half_frequency, y axis = m_sp_data_half_abs   updated

        ######################## Manipulated IFFT WAVEFORM  #########################
        re_wp_data = fftpack.ifft(m_sp_data.copy())   # len() = 9600 is CHUNK
        re_wp_data_real = np.real(re_wp_data) * 1.00   # range = [127 ~ -128] type은 float64 이다. 
        
        ########### Add Shift fre. SineWave to Manipulated IFFT WAVEFORM ############
        # volume range = 1 ~ 0
        sinewave_shift_frequency = np.sin(2*np.pi*self.SHIFT_FREQUENCY*np.linspace(0, self.SECOND_PER_FRAME, self.CHUNK)) * 125 * self.SINE_WAVE_VOLUME
        # sinwave 의 크기 범위를 127~ -128 이내로 하고 음성데이터 보다는 커야한다. 그래서 100 ~ -100 으로 한다. 
        re_wp_data_real_add_sinwave = re_wp_data_real.copy() + sinewave_shift_frequency

        ########################### Select the output data ###########################
        if self.OUTPUT_ADD_SINEWAVE == True:
            output = re_wp_data_real_add_sinwave.copy()  
            # sine + mfft 결과 # 데이터 크기 범위는 127 ~ -128 이다.
        elif self.OUTPUT_ADD_SINEWAVE == False: 
            output = re_wp_data_real.copy()          
            # sine wave 를 더하지 않고 manipulation ftt만 출력
        else: 
            print("OUTPUT_ADD_SINEWAVE=>??")

        ####################### Display to re-waveform update ########################
        self.set_plotdata(name='re_waveform', data_x=self.time, data_y=output)
        # x axis = time, y axis = re_wp_data_add_sinwave  updated

        ################################# Sound Output ###############################  
        output_int16 = (output * 32768 // 128).astype(np.int16)   
        # format이 int16 일때, int16 은 2^16 데이터 분해이므로 [ -32678 ~ 32767 ] 범위를 가져야 한다. 
        self.player.write(output_int16, self.CHUNK)
        # output을 스피커로 출력한다. 
        
        ############################ FFT Final Output data ############################
        final_output =  output.copy()
        # fft_final_output_data = fftpack.fft(np.array(final_output, dtype='int16'))
        fft_final_output_data = fftpack.fft(np.array(final_output))   
        fft_final_output_data_half_abs = np.abs(fft_final_output_data[0:int(self.CHUNK)//2]) * 2 / (128 * self.CHUNK)    

        ################### Display to add_sinewave_spectrum update ####################
        self.set_plotdata(name='add_sinewave_spectrum', data_x=self.half_frequency, data_y=fft_final_output_data_half_abs)  
        # x axis = half_frequency, y axis = fft_final_output_data_half_abs   updated


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)       # deflaut 0 
        #start(ms) animation 내의 함수 실행에 딜레이(delay)를 준다. 1000은 1000ms=1second 이다. 
        self.start()    

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


if __name__ == '__main__': 
    realtimesound = ultrasonic(RATE = 192000, BLOCKING_LOW_FREQUENCY = 500, BLOCKING_HIGH_FREQUENCY = 7000, SHIFT_FREQUENCY = 30000, OUTPUT_ADD_SINEWAVE = True, SINE_WAVE_VOLUME = 0.65)  
    # unit Hz OUTPUT_ADD_SINEWAVE = True or False #sine wave를 포함(True) or 불 포함(False)
    realtimesound.animation()



