
## Audio Input and Output from USB Microphone + Raspberry Pi
# 작동한다. 
'''
Libraries to Install 
PyAudio: Used to play and record audio on a variety of platforms. Install it by typing pip install pyaudio into the terminal 
Numpy: fundamental package for scientific computing in Python. Install it by typing pip install numpy into the terminal 



Copy the following Python script for simultaneously streaming audio output with input: 
'''
import pyaudio
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt 

print(sd.query_devices()) 
'''
 0 Microsoft 사운드 매퍼 - Input, MME (2 in, 0 out)
>  1 마이크(2- Realtek High Definiti, MME (2 in, 0 out)
   2 Microsoft 사운드 매퍼 - Output, MME (0 in, 2 out)
<  3 스피커(2- Realtek High Definiti, MME (0 in, 2 out)
   4 주 사운드 캡처 드라이버, Windows DirectSound (2 in, 0 out)
   5 마이크(2- Realtek High Definition Audio), Windows DirectSound (2 in, 0 out)
   6 주 사운드 드라이버, Windows DirectSound (0 in, 2 out)
   7 스피커(2- Realtek High Definition Audio), Windows DirectSound (0 in, 2 out)
   8 스피커(2- Realtek High Definition Audio), Windows WASAPI (0 in, 2 out)
   9 마이크(2- Realtek High Definition Audio), Windows WASAPI (2 in, 0 out)
  10 Speakers (Realtek HD Audio output), Windows WDM-KS (0 in, 8 out)
  11 스테레오 믹스 (Realtek HD Audio Stereo input), Windows WDM-KS (2 in, 0 out)
  12 마이크 (Realtek HD Audio Mic input), Windows WDM-KS (2 in, 0 out)
  13 라인 입력 (Realtek HD Audio Line input), Windows WDM-KS (2 in, 0 out)
'''

#The following code comes from markjay4k as referenced below

chunk=4096 *2 
RATE=44100

p=pyaudio.PyAudio()

#input stream setup
stream=p.open(format = pyaudio.paInt16,rate=RATE,channels=1, input_device_index = 1, input=True, frames_per_buffer=chunk)

#the code below is from the pyAudio library documentation referenced below
#output stream setup
player=p.open(format = pyaudio.paInt16,rate=RATE,channels=1, output_device_index = 3,output=True, frames_per_buffer=chunk)


while True:            #Used to continuously stream audio
   data=np.fromstring(stream.read(chunk,exception_on_overflow = False),dtype=np.int16)  
   # int16은 format이 int16 일때, int16 은 2^16 데이터 분해이므로 [ -32678 ~ 32767 ] 범위를 가져야 한다. 
   # format이 float32 일때, float32 은 데이터 범위가 [-1~1]이다. 
   player.write(data,chunk)
   print(len(data), max(data), min(data))   # chunk 맞다 
   print(np.exp(16))

# data=np.fromstring(stream.read(chunk,exception_on_overflow = False),dtype=np.int16)  
# xx = np.linspace(0,10,chunk)
# plt.plot(xx,data,',')
# plt.show()

# data=np.fromstring(stream.read(chunk,exception_on_overflow = False),dtype=np.float32)  
# xx = np.linspace(0,10,chunk)
# plt.plot(xx,data,',')
# plt.show()
   
   

#closes streams
stream.stop_stream()
stream.close()
p.terminate
