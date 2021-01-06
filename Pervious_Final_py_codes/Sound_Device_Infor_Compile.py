# https://python-sounddevice.readthedocs.io/en/0.3.7/
# sounddevice 로 sound장치들의 정보를 얻을 수 있다. 
# 장치내 sound 디바이스의 정보를 읽어 온다. 
# sounddevice 라이브러리를 이용한다. 
# 대표적으로 query_devices, query_hostapis, default.device 이 있다. 
#  query_devices는 장치 번호 대로 정렬해서 보여준다 .
# query_hostapis는 hostapi 끼리 묶어서 보여준다. 
# default.device는 현재 기본으로 되어있는 [input index, output index] 를 보여준다. 


import sounddevice as sd

# print(sd.query_devices(3, 'input'))
print(sd.query_devices(1))
print(sd.query_devices(3))
print(sd.query_hostapis())
print(sd.query_devices())
print(sd.query_devices(1))
print(sd.default.device) # default device index
print(sd.default.device[0]) # input_index 
print(sd.default.device[1]) # output_index 


