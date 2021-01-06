# by python, Inventer: Ji-ung Kim
# ultrasonic_sound_speaker_algorithm
# date: 2020, 10, 1 
from pyqtgraph.Qt import QtGui, QtCore 
import numpy as np
import pyqtgraph as pg
import sys
import pyaudio
import os
import struct
from scipy import fftpack
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget  # pyqt 화면창을 모니터 화면 중앙에 나타나도록 하기위해 필요한 Lib


class ultrasonic_sound_algorithm(object):
    def __init__(self, RATE = 192000 , BLOCKING_LOW_FREQUENCY = 0, BLOCKING_HIGH_FREQUENCY = 0, SHIFT_FREQUENCY = 0, OUTPUT_ADD_SINEWAVE = False, SINE_WAVE_VOLUME = 0.65, INPUT_DEVICE_INDEX =1,  OUTPUT_DEVICE_INDEX = 3):
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title="Ultrasonic Sound Algorithm Equalizer Running...")   
        self.win.resize(430, 20)            
        self.window_pop_up_at_center()       
        # pyqt 화면창을 모니터 화면 중앙에 나타나도록 하기위해 설정한 함수 
        self.win.show()
        # win 창을 모니터에 띄운다. 
        # self.win.setWindowTitle('ultrasonic_sound_equalizer') 
        # self.win.setBackground('k')                       
        # self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1)
        # self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1)
        # self.manipulation_spectrum = self.win.addPlot(title='Manipulated SPECTRUM', row=3, col=1)
        # self.add_sinewave_spectrum = self.win.addPlot(title='Manipulated and Add SineWave SPECTRUM', row=4, col=1)
        # self.re_waveform = self.win.addPlot(title='Manipulated IFFT and SineWave WAVEFORM', row=5, col=1)
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
        self.INPUT_DEVICE_INDEX = INPUT_DEVICE_INDEX
        # 입력 장치 번호 
        self.OUTPUT_DEVICE_INDEX = OUTPUT_DEVICE_INDEX   
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
            # input_device_index = self.INPUT_DEVICE_INDEX,
            frames_per_buffer= self.CHUNK
        )
        ###################### pyaudio class output instance #####################
        self.player = self.p.open(
            format= pyaudio.paInt16, 
            channels=self.CHANNELS,
            rate= self.RATE,
            output = True,
            output_device_index = self.OUTPUT_DEVICE_INDEX,
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
        # print(sd.default.device) # default device index
        # # 현재 연결된 input, output 장치 번호를 출력한다. 
        # print(sd.default.device[0]) # input_index 
        # print(sd.default.device[1]) # output_index 

    def window_pop_up_at_center(self):
        # pyqt 화면창을 모니터 화면 중앙에 나타나도록 하기위해 설정한 함수
        win_info = self.win.frameGeometry()
        # 정의한 창 win의 위치와 크기 정보를 가져온다. 
        moniter_info = QDesktopWidget().availableGeometry().center()
        # 사용하는 모니터 화면의 가운데 위치를 파악한다. 
        win_info.moveCenter(moniter_info)
        # 창 win의 직사각형 위치를 화면의 중심으로 위치로 이동합니다. 
        self.win.move(win_info.topLeft())  #bottomLeft, topRigth 등 가능하다. 
        # 현재 창을, 화면의 중심으로 이동했던 직사각형(win_info)의 위치로 이동시킵니다.
        # 결과적으로 현재 창의 중심이 화면의 중심과 일치하게 돼서 창이 가운데에 나타납니다. 

    # def set_plotdata(self, name, data_x, data_y):
    #     if name in self.traces:
    #         self.traces[name].setData(data_x, data_y)
    #     else:
    #         if name == 'waveform':
    #             self.traces[name] = self.waveform.plot(pen='y') 
    #             self.waveform.setYRange(-255, 255, padding=0.0)
    #             self.waveform.setXRange(0, self.SECOND_PER_FRAME, padding=0.02)
    #             self.waveform.setLabel('left', "Amplitude",)   
    #             self.waveform.setLabel('bottom', "Time", units='s') 
    #         if name == 'spectrum':
    #             self.traces[name] = self.spectrum.plot(pen='c')
    #             self.spectrum.setYRange(0, 0.4, padding=0.05)             
    #             self.spectrum.setXRange(0, self.RATE//2, padding=0.01)   
    #             self.spectrum.setLabel('left', "Amplitude",)   
    #             self.spectrum.setLabel('bottom', "Frequency", units='Hz') 
    #         if name == 'manipulation_spectrum':
    #             self.traces[name] = self.manipulation_spectrum.plot(pen='m')
    #             self.manipulation_spectrum.setYRange(0, 0.4, padding=0.05)       
    #             self.manipulation_spectrum.setXRange(0, self.RATE//2, padding=0.01)   
    #             self.manipulation_spectrum.setLabel('left', "Amplitude",)   
    #             self.manipulation_spectrum.setLabel('bottom', "Frequency", units='Hz') 
    #         if name == 'add_sinewave_spectrum':
    #             self.traces[name] = self.add_sinewave_spectrum.plot(pen='g')
    #             self.add_sinewave_spectrum.setYRange(0, 0.4, padding=0.05)       
    #             self.add_sinewave_spectrum.setXRange(0, self.RATE//2, padding=0.01)   
    #             self.add_sinewave_spectrum.setLabel('left', "Amplitude",)   
    #             self.add_sinewave_spectrum.setLabel('bottom', "Frequency", units='Hz') 
    #         if name == 're_waveform':
    #             self.traces[name] = self.re_waveform.plot(pen='w')  # pen is color
    #             self.re_waveform.setYRange(-255, 255, padding=0.0)
    #             self.re_waveform.setXRange(0, self.SECOND_PER_FRAME, padding=0.02)
    #             self.re_waveform.setLabel('left', "Amplitude",)   
    #             self.re_waveform.setLabel('bottom', "Time", units='s') 
    
    def update(self):
        ############################# Waveform data  ###################################
        wf_data = self.stream.read(self.CHUNK, exception_on_overflow = False)  
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)   
        wf_data = np.array(wf_data, dtype='b')[::2]  
        ########################## Display to waveform update ##########################
        # self.set_plotdata(name='waveform', data_x=self.time, data_y=wf_data)   
        ############################## FFT data  ######################################
        sp_data = fftpack.fft(np.array(wf_data))   
        sp_data_half_abs = np.abs(sp_data[0:int(self.CHUNK)//2]) * 2 / (128 * self.CHUNK)    
        ########################## Display to spectrum update ##########################
        # self.set_plotdata(name='spectrum', data_x=self.half_frequency, data_y=sp_data_half_abs)  
        ############################# Manipulating FFT data  #############################
        m_sp_data = sp_data.copy() 
        if self.BLOCKING_LOW_FREQUENCY == 0:  
            pass
        else:
            m_sp_data[0:int(self.BLOCKING_LOW_FREQUENCY)//int(self.FRE_RESOLUTION)+1] = 0
        if self.BLOCKING_HIGH_FREQUENCY == 0 : 
            pass
        else : 
            m_sp_data[int(self.BLOCKING_HIGH_FREQUENCY)//int(self.FRE_RESOLUTION):] = 0
        if self.SHIFT_FREQUENCY == 0 : 
            pass
        else:
            m_sp_data[int(self.RATE)//(2*int(self.FRE_RESOLUTION)):] = 0 
            m_sp_data[int(self.SHIFT_FREQUENCY) // int(self.FRE_RESOLUTION) : (int(self.RATE)//(2*int(self.FRE_RESOLUTION))+int(self.SHIFT_FREQUENCY) // int(self.FRE_RESOLUTION) )] = m_sp_data[0: int(self.RATE)//(2*int(self.FRE_RESOLUTION))]
            m_sp_data[:int(self.SHIFT_FREQUENCY)//int(self.FRE_RESOLUTION)] = 0
        m_sp_data_half_abs = np.abs(m_sp_data[:int(self.CHUNK)//2]) * 2 / (128 * self.CHUNK)    
        ################# Display to manipulation_spectrum update ###################
        # self.set_plotdata(name='manipulation_spectrum', data_x=self.half_frequency, data_y=m_sp_data_half_abs)  
        ######################## Manipulated IFFT WAVEFORM  #########################
        re_wp_data = fftpack.ifft(m_sp_data.copy())  
        re_wp_data_real = np.real(re_wp_data) * 1.00  
        ########### Add Shift fre. SineWave to Manipulated IFFT WAVEFORM ############
        sinewave_shift_frequency = np.sin(2*np.pi*self.SHIFT_FREQUENCY*np.linspace(0, self.SECOND_PER_FRAME, self.CHUNK)) * 125 * self.SINE_WAVE_VOLUME
        re_wp_data_real_add_sinwave = re_wp_data_real.copy() + sinewave_shift_frequency
        ########################### Select the output data ###########################
        if self.OUTPUT_ADD_SINEWAVE == True:
            output = re_wp_data_real_add_sinwave.copy()   
        elif self.OUTPUT_ADD_SINEWAVE == False: 
            output = re_wp_data_real.copy()          
        else: 
            print("OUTPUT_ADD_SINEWAVE=>??")
        ####################### Display to re-waveform update ########################
        # self.set_plotdata(name='re_waveform', data_x=self.time, data_y=output)
        ################################# Sound Output ###############################  
        output_int16 = (output * 32768 // 128).astype(np.int16)   
        self.player.write(output_int16, self.CHUNK)
        ############################ FFT Final Output data ############################
        final_output =  output.copy()
        fft_final_output_data = fftpack.fft(np.array(final_output))   
        fft_final_output_data_half_abs = np.abs(fft_final_output_data[0:int(self.CHUNK)//2]) * 2 / (128 * self.CHUNK)    
        ################### Display to add_sinewave_spectrum update ####################
        # self.set_plotdata(name='add_sinewave_spectrum', data_x=self.half_frequency, data_y=fft_final_output_data_half_abs)  
    
    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)      
        # sys.exit(self.app.exec_())  # 이걸 쓴다. 
        self.start()                  # 위것을 써도 되고 아래꺼 써도 된다.

    ## PYQT Equalizer 실행에 필요한것 
    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

###################################### Program Start by Module ###################################
def algorithm_start_func(RATE, BLOCKING_LOW_FREQUENCY, BLOCKING_HIGH_FREQUENCY, SHIFT_FREQUENCY, OUTPUT_ADD_SINEWAVE, SINE_WAVE_VOLUME,  INPUT_DEVICE_INDEX ,  OUTPUT_DEVICE_INDEX):
     
    ultrasonic_sound = ultrasonic_sound_algorithm(RATE, BLOCKING_LOW_FREQUENCY, BLOCKING_HIGH_FREQUENCY, SHIFT_FREQUENCY, OUTPUT_ADD_SINEWAVE, SINE_WAVE_VOLUME,  INPUT_DEVICE_INDEX,  OUTPUT_DEVICE_INDEX)  
    ultrasonic_sound.animation()

#################################### Program Start itself ###########################################
if __name__ == '__main__': 
    Enter_INPUT_DEVICE_INDEX = sd.default.device[0]
    # Default input_index를 입력
    Enter_OUTPUT_DEVICE_INDEX = sd.default.device[1]
    # Default output_index를 입력 

    ultrasonic_sound = ultrasonic_sound_algorithm(RATE = 192000, BLOCKING_LOW_FREQUENCY = 500, BLOCKING_HIGH_FREQUENCY = 7000, SHIFT_FREQUENCY = 30000, OUTPUT_ADD_SINEWAVE = True, SINE_WAVE_VOLUME = 0,  INPUT_DEVICE_INDEX = Enter_INPUT_DEVICE_INDEX ,  OUTPUT_DEVICE_INDEX = Enter_OUTPUT_DEVICE_INDEX)  
    # unit = Hz 
    ultrasonic_sound.animation()

