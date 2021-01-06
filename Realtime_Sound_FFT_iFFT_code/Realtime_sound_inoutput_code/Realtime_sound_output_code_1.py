
## https://www.thetopsites.net/article/53843447.shtml

## Generating sine wave sound in python 

# 진짜로 출력이 된다. 

import pyaudio
import numpy as np
import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

volume = 1   #range 0 ~ 1.0

fs = 192000    # sampling frequency Hz

duration = 3.0   # in second may be float

f = 440.0      # sine wave Hz 

sample = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
# np.float32 는 32bit 파일 이란 소리다. 이는 [-1~1]영역의데이터가 있어야한다. 
stream = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=fs,
    output=True
    )


# sample = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.int16)  # int 16으로 바꾸니까 작동을 안한다.....

# stream = p.open(
#     format= pyaudio.paInt16,
#     channels=1,
#     rate=fs,
#     output=True
#     )

# sample = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.int16)  # int 16으로 바꾸니까 작동을 안한다.....

# stream = p.open(
#     format= pyaudio.paInt16,
#     channels=1,
#     rate=fs,
#     output=True
#     )



stream.write(volume*sample)

stream.stop_stream()
stream.close()

p.terminate()
print(np.arange(fs*duration))
print(sample, len(sample))
plt.plot(np.linspace(0,10,len(sample)),sample,',')
plt.show()