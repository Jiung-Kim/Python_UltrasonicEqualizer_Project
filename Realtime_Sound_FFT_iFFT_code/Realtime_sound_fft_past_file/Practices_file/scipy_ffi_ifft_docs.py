import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack as fftpk
import numpy as np
import scipy.fft
import matplotlib.pyplot as plt
import numpy as np

# %matplotlib tk 

s_rate, signal = wavfile.read("tibet.wav")  #fs=48000Hz,  769275 samples
time1 = np.linspace(0, 16, 769275)     
time2 = np.linspace(0, 16, len(signal)//2)

sfft = scipy.fft(signal)
halfsfft = sfft[:len(signal)//2] 
ihalfsfft = scipy.fft.ifft(halfsfft)
isfft = scipy.fft.ifft(sfft)
# plt.plot(time1, signal,'.', time2, ihalfsfft,'--') # ftt fs를 절반만 써도 정확하게 일치한다. 
plt.plot(time1,signal,'.',time1,isfft,'--')  # 정확하게 일치한다. 
plt.show()