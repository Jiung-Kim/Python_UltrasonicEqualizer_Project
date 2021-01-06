"""
최종 수정일: 2020.10.14 
python 개발 환경(Development Environment)
python 3.8.5-64bit 
module -> requirements.txt의 목록에 있다. 
txt 의 목록을 바로 설치하는 방법은 pip install -r requirements.txt 

"""
### PyFile Name : Main_for_Ultrasonic_sound_algorithm_final_2020_10_14_ver
### No Description Version
import GUI_For_Ultra_Algorithm_2020_10_15_ver
import Ultra_Algorithm_2020_10_15_ver
import sys 
import os

### GUI And Ultrasonic sound algorithm modules 
GUI_for_Ultrasonic_sound_algorithm_module = GUI_For_Ultra_Algorithm_2020_10_15_ver
Ultrasonic_sound_algorithm_module = Ultra_Algorithm_2020_10_15_ver

def Restart_Program_func():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)  # 이것으로 Exe 프로그램이 재시작한다. 

if __name__ == '__main__': 
    try:
        print("Ultrasonic Sound Speaker GUI이 시작합니다.")
        GUI_display = GUI_for_Ultrasonic_sound_algorithm_module.Ultrasonic_sound_GUI() #파일 이름 과 class 이름 
        GUI_display.program_start()                                                    # UI 모듈 시작하기 
        print("Ultrasonic Sound Algorithm Setting Valus를 가져옵니다.")                # class 내의 함수 시작 
        Setting_values = GUI_display.start_func()                

        Ultrasonic_UI_View_Counter = 0

        while True: 
            Ultrasonic_UI_View_Counter += 1
            print("While 문에서의 Ultrasonic_UI_View_Counter는 :", Ultrasonic_UI_View_Counter)
            print("Ultrasonic Sound Algorithm를 시작합니다.") 
            globals()['Ultrasonic_sound_algorithm_class_name_{0}'.format(Ultrasonic_UI_View_Counter)] = Ultrasonic_sound_algorithm_module.ultrasonic_sound_algorithm(RATE=Setting_values[0], BLOCKING_LOW_FREQUENCY=Setting_values[2], BLOCKING_HIGH_FREQUENCY=Setting_values[3], SHIFT_FREQUENCY=Setting_values[4], OUTPUT_ADD_SINEWAVE=Setting_values[7], SINE_WAVE_VOLUME=Setting_values[8],  INPUT_DEVICE_INDEX=Setting_values[5], OUTPUT_DEVICE_INDEX=Setting_values[6])

            globals()['Ultrasonic_sound_algorithm_class_name_{0}'.format(Ultrasonic_UI_View_Counter)].program_start()
            globals()['Ultrasonic_sound_algorithm_class_name_{0}'.format(Ultrasonic_UI_View_Counter)].program_exit()

    except OSError: 
        print("----------------Audio Device index Error----------------")
        GUI_display.error_Label_TERMINAL_display()
        print("R E S T A R T 버튼을 누르면 프로그램이 재시작합니다.")
        GUI_display.program_start() 
        print("프로그램이 재시작합니다.")
        Restart_Program_func()       # 오류 발생시 프로그램을 재시작한다. 이것으로 Exe 프로그램이 재시작한다. 

        
        







        

