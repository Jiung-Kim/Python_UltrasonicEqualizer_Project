### PyFile Name : GUI_for_Ultrasonic_sound_algorithm_final_2020_10_14_ver
### No Description Version
import sys 
import os
import csv 
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLineEdit, QInputDialog, QPushButton, QFrame, QLabel
from PyQt5.QtCore import Qt, QCoreApplication
from pyqtgraph.Qt import QtGui, QtCore
import sounddevice as sd
###################################### Ultrasonic Sound Speaker GUI CLASS ####################################################################################
class Ultrasonic_sound_GUI(QWidget):

    def __init__(self):
        self.app = QApplication(sys.argv)    
        super().__init__()
        self.initUI()

    def initUI(self):
        ############################ Default pyaudio Setting Values ##############################
        IN_OUTPUT_RATE = 192000                    # 0
        FRE_Res = 20                               # 1 
        BLOCKING_LOW_FREQUENCY = 0                 # 2
        BLOCKING_HIGH_FREQUENCY = 20000            # 3
        SHIFT_FREQUENCY = 30000                    # 4
        INPUT_DEVICE_INDEX = sd.default.device[0]  # 5 
        OUTPUT_DEVICE_INDEX = sd.default.device[1] # 6 
        OUTPUT_ADD_SINEWAVE = True                 # 7  
        SINE_WAVE_VOLUME = 0.70                    # 8
        
        ############################## Setting Values List  #####################################
        self.setting_values = [IN_OUTPUT_RATE, FRE_Res, BLOCKING_LOW_FREQUENCY, BLOCKING_HIGH_FREQUENCY, SHIFT_FREQUENCY, INPUT_DEVICE_INDEX, OUTPUT_DEVICE_INDEX, OUTPUT_ADD_SINEWAVE, SINE_WAVE_VOLUME]

        ############################ Create the Setting Values TXT file #########################
        try:
            setting_values_read = open("Ultrasonic_algorithm_setting_values.csv", 'r', encoding='utf-8')
            csv_read = csv.reader(setting_values_read)
            for setlist in csv_read:
                # print(setlist)
                self.read_setting_values_list = setlist
                break
            setting_values_read.close()
            
            ### Convert str to int, str to bool 
            for index in list(range(0, 9)):
                if index == 7:
                    if self.read_setting_values_list[index] == 'True' or self.read_setting_values_list[index] == True  :
                        self.read_setting_values_list[index] = True
                    
                    elif self.read_setting_values_list[index] == 'False' or read_setting_values_list[index] == False:
                        self.read_setting_values_list[index] = False
                      
                    else:
                        print("ERROR : Sine Wave output On/Off Component Error") 

                elif index == 8:
                    self.read_setting_values_list[index] = float(self.read_setting_values_list[index])
                else:
                    self.read_setting_values_list[index] = int(self.read_setting_values_list[index])
                  
            ### Change Default Setting values to Import saved Setting values
            self.setting_values = self.read_setting_values_list 

        except:
            print("There is No Saved Setting Values csv file")
            pass 

        ################################# Control GUI View #########################################
        ### Program Name
        Label_NAME = QLabel('ULTRASONIC SOUND SPEAKER GENERATOR', self)
        Label_NAME.setFont(QtGui.QFont("Time", 15, QtGui.QFont.Bold))  
        Label_NAME.move(35, 10)

        ### Sampling Frequency Set
        Label_RATE_name = QLabel('Input and Output Sampling Frequency Set', self)
        Label_RATE_name.setFont(QtGui.QFont("Time", 12, QtGui.QFont.Bold))  # 폰트 변환
        Label_RATE_name.setStyleSheet("Color : green")
        Label_RATE_name.move(90, 40)

        self.btn_RATE_192000 = QPushButton('Set S. Fre. : 192.000 Hz', self)
        self.btn_RATE_192000.resize(150, 30)
        self.btn_RATE_192000.move(10, 65)
        self.btn_RATE_192000.clicked.connect(self.in_out_rate_192000hz)
        self.btn_RATE_96000 = QPushButton('Set S. Fre. : 96.000 Hz', self)
        self.btn_RATE_96000.resize(150, 30)
        self.btn_RATE_96000.move(170, 65)
        self.btn_RATE_96000.clicked.connect(self.in_out_rate_96000hz)
        self.Label_RATE_display = QLabel('Default S. Frequency Value:\n       {0} Hz'.format(self.setting_values[0]), self)
        self.Label_RATE_display.resize(160, 30)
        self.Label_RATE_display.move(330,65)

        #### Input and Output Device selection
        self.Label_INDEX_name = QLabel('Input and Output Audio Devices index Set', self)
        self.Label_INDEX_name.setFont(QtGui.QFont("Time", 12, QtGui.QFont.Bold))  
        self.Label_INDEX_name.setStyleSheet("Color :blue")
        self.Label_INDEX_name.move(95, 105)

        self.INDEX_frame = QFrame(self)
        self.INDEX_frame.setStyleSheet("QWidget { background-color: teal} ")
        self.INDEX_frame.resize(450, 260)
        self.INDEX_frame.move(25, 130)

        audio_info = str(sd.query_devices())  # Get audio device info. 
        self.Label_audio_info_display = QLabel("Current Audio Device List: \n" + audio_info, self)
        self.Label_audio_info_display.setFont(QtGui.QFont("Consolas", 9, QtGui.QFont.Thin))  
        self.Label_audio_info_display.setStyleSheet("Color : black")
        self.Label_audio_info_display.resize(450, 260)
        self.Label_audio_info_display.move(25, 120)

        self.btn_INPUT_INDEX = QPushButton('Input Device index set', self)
        self.btn_INPUT_INDEX.resize(150, 30)
        self.btn_INPUT_INDEX.move(10, 400)
        self.btn_INPUT_INDEX.clicked.connect(self.in_device_index)
        self.btn_OUT_INDEX = QPushButton('Output Device index set', self)
        self.btn_OUT_INDEX.resize(150, 30)
        self.btn_OUT_INDEX.move(170, 400)
        self.btn_OUT_INDEX.clicked.connect(self.out_device_index)
        self.Label_INDEX_display = QLabel('Default In,Out Device index:\n            {0}, {1}'.format(self.setting_values[5], self.setting_values[6]), self)
        self.Label_INDEX_display.resize(170, 30)
        self.Label_INDEX_display.move(322 ,400)
        
        ### Cut the Low Frequency and high Frequency Set
        self.Label_CUT_name = QLabel('Cut the Low and High Frequency Set', self)
        self.Label_CUT_name.setFont(QtGui.QFont("Time", 12, QtGui.QFont.Bold))  
        self.Label_CUT_name.setStyleSheet("Color : orange")
        self.Label_CUT_name.move(110, 440)

        self.btn_CUTLOW = QPushButton('Low Frequency(below) Set', self)
        self.btn_CUTLOW.resize(200, 30)
        self.btn_CUTLOW.move(40, 470)
        self.btn_CUTLOW.clicked.connect(self.low_fre)
        self.btn_CUTHIGH = QPushButton('High Frequency(above) Set', self)
        self.btn_CUTHIGH.resize(200, 30)
        self.btn_CUTHIGH.move(260, 470)
        self.btn_CUTHIGH.clicked.connect(self.high_fre)

        self.Label_CUTLOW_display = QLabel('Default Cut the Low Fre.: {0} Hz'.format(self.setting_values[2]), self)
        self.Label_CUTLOW_display.resize(230, 30)
        self.Label_CUTLOW_display.move(35 ,500)
        self.Label_CUTHIGH_display = QLabel('Default Cut the High Fre.: {0} Hz'.format(self.setting_values[3]), self)
        self.Label_CUTHIGH_display.resize(230, 30)
        self.Label_CUTHIGH_display.move(265 ,500)

        ### Sine Wave Frequnecy and Volume Set
        self.Label_SINEWAVE_name = QLabel('Sine Wave Frequency and Volume Set', self)
        self.Label_SINEWAVE_name.setFont(QtGui.QFont("Time", 12, QtGui.QFont.Bold))  
        self.Label_SINEWAVE_name.setStyleSheet("Color : red")
        self.Label_SINEWAVE_name.move(105, 530)

        self.btn_SINEWAVE_FRE = QPushButton('Sine Wave Frequency Set', self)
        self.btn_SINEWAVE_FRE.resize(200, 30)
        self.btn_SINEWAVE_FRE.move(40, 560)
        self.btn_SINEWAVE_FRE.clicked.connect(self.sine_fre)
        self.btn_SINEWAVE_VOL = QPushButton('Sine Wave Volume Set', self)
        self.btn_SINEWAVE_VOL.resize(200, 30)
        self.btn_SINEWAVE_VOL.move(260, 560)
        self.btn_SINEWAVE_VOL.clicked.connect(self.sine_vol)

        self.Label_SINEWAVE_FRE_display = QLabel('Default Sine Wave Fre.: {0} Hz'.format(self.setting_values[4]), self)
        self.Label_SINEWAVE_FRE_display.resize(230, 30)
        self.Label_SINEWAVE_FRE_display.move(35 ,590)
        self.Label_SINEWAVE_VOL_display = QLabel('Default Sine Wave Vol.: {0}'.format(self.setting_values[8]), self)
        self.Label_SINEWAVE_VOL_display.resize(230, 30)
        self.Label_SINEWAVE_VOL_display.move(265 ,590)

        #### START Generate a Real Time Ultrasonic Sound Action
        self.Label_START_name = QLabel('START To Generate a Real Time Ultrasonic Sound', self)
        self.Label_START_name.setFont(QtGui.QFont("Time", 14, QtGui.QFont.Bold))  
        self.Label_START_name.setStyleSheet("Color : purple")
        self.Label_START_name.move(20, 620)

        self.btn_START = QPushButton('S T A R T', self)
        self.btn_START.resize(200, 40)
        self.btn_START.move(40, 650)
        self.btn_START.clicked.connect(self.start_func)

        self.btn_STOP = QPushButton('P R O G R A M - E X I T\nSave the Setting Vaules', self)
        self.btn_STOP.resize(200, 40)
        self.btn_STOP.move(260, 650)
        self.btn_STOP.clicked.connect(self.exit_func)

        ### Setting values display 
        self.TERMINAL_display_frame = QFrame(self)
        self.TERMINAL_display_frame.setStyleSheet("QWidget { background-color: silver} ")
        # self.TERMINAL_display_frame.resize(484, 65)
        self.TERMINAL_display_frame.move(8, 700)
        self.TERMINAL_display_frame.resize(484, 100)

        self.Label_TERMINAL_display = QLabel(" Ultrasonic Sound Speaker Algorithm Software에 오신것을 환영합니다.\n이 프로그램은 인간의 귀에 초음파를 통해 소리를 들리게 해주는\n기술이 구현되어 있습니다.\n더욱 자세한 내용은 이 프로그램의 개발자이자 발명가이자 물리학자인\nJiung Kim(jiungsapple@gmail.com)에게 문의 주십시오.\n그리고 이 프로그램에 구현된 기술은 한국 특허로 보호 받고 있습니다.", self)
        self.Label_TERMINAL_display.resize(480, 100)
        self.Label_TERMINAL_display.move(10, 700)
        # self.Label_TERMINAL_display = QLabel(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]), self)
        # self.Label_TERMINAL_display.resize(480, 55)
        # self.Label_TERMINAL_display.move(15, 705)

        ############################### GUI basic Setting and Show ##############################################
        self.setGeometry(0, -200, 500, 780)
        # self.resize(500, 780)
        self.resize(500, 805)
        self.window_pop_up_at_center()      
        self.setWindowTitle("Ultrasonic Sound Speaker Control Panel")
        self.showing_Timer = 0 
        self.showing_Timer_time_out = 15 # second
        self.showing_Timer_time_reverse_counter = 15 
        self.show()

    ############################################### GUI Functions ###############################################
    def setting_values_save_csv(self):
        setting_values_write = open('Ultrasonic_algorithm_setting_values.csv', 'w', encoding='utf-8')
        csv_writer = csv.writer(setting_values_write)
        csv_writer.writerow(self.setting_values)
        setting_values_write.close()
    
    def gui_Timer(self):      
        self.showing_Timer += 1
        print("Ultrasonic Sound Speaker Control Panel Showing Time(s): ",self.showing_Timer)
        
        if self.showing_Timer > self.showing_Timer_time_out:
            print("start_func is going(GUI)")
            self.start_func()
        elif self.showing_Timer <= self.showing_Timer_time_out:
            self.time_left = self.showing_Timer_time_reverse_counter - self.showing_Timer
            
            self.btn_START.setText('S T A R T \n After {0} sec. Automatic operation'.format(self.time_left))

    def gui_Timer_check(self):
        if self.showing_Timer <= self.showing_Timer_time_out:
            self.showing_Timer = 0

    def mouseMoveEvent(self, event):
        mouse_pt = "Mouse Point : x={0},y={1}, global={2},{3}".format(event.x(), event.y(), event.globalX(), event.globalY())
        if mouse_pt != None:
            if self.showing_Timer <= self.showing_Timer_time_out:
                self.showing_Timer = 0
                
    def mousePressEvent(self, event):
        self.Click = None
        if event.button() & Qt.LeftButton:
            self.Click = 'LEFT_Mouse'
            if self.showing_Timer <= self.showing_Timer_time_out:
                self.showing_Timer = 0
                print(self.Click)

        if event.button() & Qt.MidButton:
            self.Click = 'MIDDLE_Mouse'
            if self.showing_Timer <= self.showing_Timer_time_out:
                self.showing_Timer = 0
                print(self.Click)

        if event.button() & Qt.RightButton:
            self.Click = 'RIGHT_Mouse'
            if self.showing_Timer <= self.showing_Timer_time_out:
                self.showing_Timer = 0
                print(self.Click)
            
    def error_Label_TERMINAL_display(self):
        self.Label_TERMINAL_display.setText("                              -------Audio Device index Error------- \n                      Please Certification the In, Out Device index Number\n                When Press the [S T A R T] Button, Program is re-starting") 
        

    def window_pop_up_at_center(self):
        win_info = self.frameGeometry()
        moniter_info = QDesktopWidget().availableGeometry().center()
        win_info.moveCenter(moniter_info)
        self.move(win_info.topRight()) 
    
    def in_out_rate_192000hz(self):
        self.gui_Timer_check()
        self.Label_RATE_display.setText('Set S. Frequency Value:\n             {0} Hz'.format('192,000'))
        self.setting_values[0] = int(192000)
        self.setting_values[1] = int(20)
        self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))

    def in_out_rate_96000hz(self):
        self.gui_Timer_check()
        self.Label_RATE_display.setText('Set S. Frequency Value:\n             {0} Hz'.format('96,.000'))
        self.setting_values[0] = int(96000)
        self.setting_values[1] = int(10)
        self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))

    def in_device_index(self):
        self.gui_Timer_check()
        in_index, ok = QInputDialog.getText(self, 'Input Device index Set', 'Type the index value: ')

        if ok:
            if not in_index:
                self.Label_INDEX_display.setText('       Er:Typing Number\n          of Device index')
            elif int(in_index):
                self.Label_INDEX_display.setText('In, Out Device index: \n           {0}, {1} '.format(in_index, self.setting_values[6]))
                self.setting_values[5] = int(in_index)
                self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))
            else:
                self.Label_INDEX_display.setText('       Er:Typing Number\n          of Device index')

    def out_device_index(self):
        self.gui_Timer_check()
        out_index, ok = QInputDialog.getText(self, 'Output Device index Set', 'Type the index value: ')
        if ok:
            if not out_index:
                self.Label_INDEX_display.setText('       Er:Typing Number\n          of Device index')
            elif int(out_index):
                self.Label_INDEX_display.setText('In, Out Device index: \n           {0}, {1} '.format(self.setting_values[5], out_index))
                self.setting_values[6] = int(out_index)
                self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))
            else:
                self.Label_INDEX_display.setText('       Er:Typing Number\n          of Device index')
    
    def low_fre(self):
        self.gui_Timer_check()
        low_fre, ok = QInputDialog.getText(self, 'Low Frequency Set', 'Type the Frequency(mainly 0 ~ 500) (Hz):')

        if ok:
            if not low_fre:
                self.Label_CUTLOW_display.setText('Er:Typing Number of value: 0 to 30,000')
            else:
                if float(low_fre) >= 0 and float(low_fre) <= 30000 : 
                    self.Label_CUTLOW_display.setText('Low Fre.: {0} Hz'.format(low_fre))
                    self.setting_values[2] = int(low_fre)
                    self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))
                else:
                    self.Label_CUTLOW_display.setText('Er:Typing Number of value: 0 to 30,000')

    def high_fre(self):
        self.gui_Timer_check()
        high_fre, ok = QInputDialog.getText(self, 'High Frequency Set', 'Type the Frequency(mainly 2,000 ~ 15,000) (Hz):')
        if ok:
            if not high_fre:
                self.Label_CUTHIGH_display.setText('Er:Typing Number of value: 0 to 30,000')
            else:
                if float(high_fre) > 0 and float(high_fre) <= 30000 :
                    self.Label_CUTHIGH_display.setText('High Fre.: {0} Hz'.format(high_fre))
                    self.setting_values[3] = int(high_fre)
                    self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))
                elif float(high_fre) == 0:
                    self.Label_CUTHIGH_display.setText('Not Cut the High Fre. ')
                    self.setting_values[3] = int(high_fre)
                    self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))
                else:
                    self.Label_CUTHIGH_display.setText('Er:Typing Number of value: 0 to 30,000')

    def sine_fre(self):
        self.gui_Timer_check()
        sine_fre, ok = QInputDialog.getText(self, 'Sine Wave Frequency Set', 'Type the Frequency(mainly 25,000 ~ 40,000) (Hz):')
        print(sine_fre,    type(sine_fre))
        if ok:
            if not sine_fre: 
                self.Label_SINEWAVE_FRE_display.setText('Er:Typing Number of Value: 0 to 45,000')
            else:
                if float(sine_fre) >= 0 and float(sine_fre) <= 45000 :
                    self.Label_SINEWAVE_FRE_display.setText('Sine Wave Fre.: {0} Hz'.format(sine_fre))
                    self.setting_values[4] = int(sine_fre)
                    self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))
                else:
                    self.Label_SINEWAVE_FRE_display.setText('Er:Typing Number of Value: 0 to 45,000')
            
    def sine_vol(self):
        self.gui_Timer_check()
        sine_vol, ok = QInputDialog.getText(self, 'Sine Wave Volume Set', 'Type the Volume(0 ~ 1): ')

        if ok:
            if not sine_vol: 
                self.Label_SINEWAVE_VOL_display.setText('Er:Typing Number of Value: 0 to 1')
            else:
                if float(sine_vol) > 0 and float(sine_vol) <= 1 : 
                    self.Label_SINEWAVE_VOL_display.setText('Sine Wave Vol.: {0}'.format(sine_vol))
                    self.setting_values[8] = float(sine_vol)
                    self.setting_values[7] = True
                    self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))
                
                elif float(sine_vol) == 0 : 
                    self.Label_SINEWAVE_VOL_display.setText('Sine Wave Vol.: {0}'.format(sine_vol))
                    self.setting_values[7] = False
                    self.setting_values[8] = int(0)
                    self.Label_TERMINAL_display.setText(" SETTING VALUES VIEWER: \n In, Output S. Fre.: [{0}] Hz, SineWave Fre.: [{1}] Hz,  SineWave Vol.: [{2}] \n Cut Low(below) Fre.: [{3}] Hz, Cut High(above) Fre.:[{4}] Hz \n Input Device index: [{5}], Output Device index: [{6}]".format(self.setting_values[0],self.setting_values[4], self.setting_values[8],self.setting_values[2],self.setting_values[3], self.setting_values[5], self.setting_values[6]))
                else :
                    self.Label_SINEWAVE_VOL_display.setText('Er:Typing Number of Value: 0 to 1')

    def start_func(self):
        # print("Export the Setting_Values:", self.setting_values)
        ### Start Button act to Save at Setting Values 
        # print("Setting Values를 csv file에 저장합니다.")
        # self.btn_START.setText('R E S T A R T\n Setting Values were Saved')
        # self.setting_values_save_csv()   # txt 파일 작성하는 함수
        #### Start Button act to sign the Button Label
        self.btn_START.setText('R E S T A R T')
        QApplication.exit()  

        return self.setting_values    # Output the Setting Values
        
    def exit_func(self):    
        print("Export the Setting_Values:", self.setting_values)
        print("Setting Values를 csv file에 저장합니다.")
        self.setting_values_save_csv()                 # txt 파일 작성하는 함수
        print("프로그램을 종료합니다.")
        sys.exit()                                     #  파이선 프로그램 종료 
        os._exit()
    

    ####################################### GUI Start Function by Module #############################
    def program_start(self):
        timer = QtCore.QTimer()
        # timer.setInterval(1000)  # Interval이 작동안한다. 
        timer.timeout.connect(self.gui_Timer)
        timer.start(1000)      # ms 단위로 interval 이 작동한다.

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QApplication.instance().exec_()
            
