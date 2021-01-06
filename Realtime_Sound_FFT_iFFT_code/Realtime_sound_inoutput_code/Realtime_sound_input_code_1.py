
##
##
## https://kcal2845.tistory.com/m/35
## pyaudio 로 음성 데이터 입력받기 

import pyaudio 
import numpy as np 

CHUNK = 2**10  # 2^10 = 1024 
# print(CHUNK)
RATE = 44100  # hz

p=pyaudio.PyAudio()

stream=p.open(format=pyaudio.paInt16, 
    channels=1, 
    rate=RATE, 
    input=True, 
    frames_per_buffer=CHUNK
    )  # input_divice_indix=2

while(True):
    data = np.fromstring(stream.read(10), dtype=np.int16)   # CHUNK 길이 
    print(int(np.average(np.abs(data))))

stream.stop_stream()
stream.close()
p.terminate()
