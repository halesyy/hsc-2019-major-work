#!/usr/bin/env python3
import pyaudio
import struct
import math
import time
from multiprocessing import Process

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()


def data_for_freq(frequency: float, time: float = None):
    """get frames for a fixed frequency for a specified time or
    number of frames, if frame_count is specified, the specified
    time is ignored"""
    frame_count = int(RATE * time)

    remainder_frames = frame_count % RATE
    wavedata = []

    for i in range(frame_count):
        a = RATE / frequency  # number of frames per wave
        b = i / a
        c = b * (2 * math.pi)
        d = math.sin(c) * 32767
        e = int(d)
        wavedata.append(e)

    for i in range(remainder_frames):
        wavedata.append(0)

    number_of_bytes = str(len(wavedata))
    wavedata = struct.pack(number_of_bytes + 'h', *wavedata)

    return wavedata


def play(frequency: float, time: float):
    """
    play a frequency for a fixed time!
    """
    frames = data_for_freq(frequency, time)
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    stream.write(frames)
    stream.stop_stream()
    stream.close()

def freqFromRoot(root=0):
    base = 82.4 # E note open
    frequency = base * (math.pow((math.pow(2, 1/12)), root))
    return round(frequency, 2)

def fret(number, t=0.25):
    if isinstance(number, list): chord(number, t)
    else: play(freqFromRoot(number), t)

def chord(numberArray, t=0.3):
    ps = []
    for number in numberArray:
        p = Process(target=fret, args=[number])
        p.start()
    time.sleep(t)
    for p in ps:
        p.join()


if __name__ == '__main__':
    fret([1,2,3])
