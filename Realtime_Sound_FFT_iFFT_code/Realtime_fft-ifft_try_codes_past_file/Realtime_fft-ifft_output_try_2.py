##https://stackoverflow.com/questions/31674416/python-realtime-audio-streaming-with-pyaudio-or-something-else


##Python: realtime audio streaming with PyAudio (or something else)?
'''
14


11
Currently I'm using NumPy to generate the WAV file from a NumPy array. I wonder if it's possible to play the NumPy array in realtime before it's actually written to the hard drive. All examples I found using PyAudio rely on writing the NumPy array to a WAV file first, but I'd like to have a preview function that just spits out the NumPy array to the audio output.

Should be cross-platform, too. I'm using Python 3 (Anaconda distribution).
'''
'''
This has worked! Thanks for help!

def generate_sample(self, ob, preview):
    print("* Generating sample...")
    tone_out = array(ob, dtype=int16)

    if preview:
        print("* Previewing audio file...")

        bytestream = tone_out.tobytes()
        pya = pyaudio.PyAudio()
        stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=OUTPUT_SAMPLE_RATE, output=True)
        stream.write(bytestream)
        stream.stop_stream()
        stream.close()

        pya.terminate()
        print("* Preview completed!")
    else:
        write('sound.wav', SAMPLE_RATE, tone_out)
        print("* Wrote audio file!")
Seems so simple now, but when you don't know Python very well, it seems like hell.

'''
'''
This is really simple with python-sounddevice:

import sounddevice as sd
sd.play(myarray, 44100)

'''
'''
As you can see in the examples, pyaudio just reads data from the WAV file and writes that to the stream.

It is not necessary to write a WAV file first, you just need a stream of data in the right format.

I'm adding the example below in case the link ever goes dead (note that I didn't write this code):

"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()

'''