#encoding=utf-8
mnot = open("./../intermediary.txt", "r+").read()

import pyaudio
import struct
import math
import numpy
import time
from multiprocessing import Process

PLAY_AUDIO_FROM_TAB = False
notePlayLength = 0.25

conversionClassifier = "! $ % & ' ( ) * + . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ ] ^ _ ` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~ ° ± ² ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾ ¿ À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï  Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý Þ ß"
conversionClassifier = conversionClassifier.split(' ')
noterPerBar = 4

# Converting matrix
converter = {}
for conv, i in zip(conversionClassifier, range(0, len(conversionClassifier))):
    converter["{0}".format(conv)] = i
backConverter = {v: k for k, v in converter.items()}

def verticalStep(v, e, B, G, D, A, E, ADDDIVIDER=False):
    # print(v)
    tE, tA, tD, tG, tB, te = "", "", "", "", "", ""
    notes = []
    # each "note" is the deconstruction of the chord piece
    for noteString in v:
        note = converter[noteString]
        notes.append(note)
        if note - 0 < 5:
            # tE, tA, tD, tG, tB, te = str(note-0)+"--", "---", "---", "---", "---", "---"
            tE += str(note-0)+"-"
        elif note - 5 < 5:
            # tE, tA, tD, tG, tB, te = "---",str(note-5)+"--", "---", "---", "---", "---"
            tA += str(note-5)+"-"
        elif note - 10 < 5:
            # tE, tA, tD, tG, tB, te = "---", "---", str(note-10)+"--", "---", "---", "---"
            tD += str(note-10)+"-"
        elif note - 15 < 5:
            # tE, tA, tD, tG, tB, te = "---", "---", "---", str(note-15)+"--", "---", "---"
            tG += str(note-15)+"-"
        elif note - 20 < 5:
            # tE, tA, tD, tG, tB, te = "---", "---", "---", "---", str(note-20)+"--", "---"
            tB += str(note-20)+"-"
        elif note - 25 < 5:
            # tE, tA, tD, tG, tB, te = "---", "---", "---", "---", "---", str(note-25)+"--"
            te += str(note-25)+"-"
        else:
            te += str(note-25)+"-"
            # tE, tA, tD, tG, tB, te = "---", "---", "---", "---", "---", str(note-25)+"-"

    if PLAY_AUDIO_FROM_TAB == True:
        fret(notes, notePlayLength)

    # finding the max str val
    mlen = 0
    for x in [tE, tA, tD, tG, tB, te]:
        if len(x) > mlen: mlen = len(x)
    # pack "-" into mlen+1
    E += tE + "-"*((mlen+2)-len(tE))
    A += tA + "-"*((mlen+2)-len(tA))
    D += tD + "-"*((mlen+2)-len(tD))
    G += tG + "-"*((mlen+2)-len(tG))
    B += tB + "-"*((mlen+2)-len(tB))
    e += te + "-"*((mlen+2)-len(te))

    if ADDDIVIDER == True:
        E += "|-"
        A += "|-"
        D += "|-"
        G += "|-"
        B += "|-"
        e += "|-"

    return [e, B, G, D, A, E]

def bar(un_notes):
    e, B, G, D, A, E = "e|--", "B|--", "G|--", "D|--", "A|--", "E|--"
    iter = 0
    for v in un_notes.split(' '):
        if len(v) >0 and v[0] == '':
            pass
        elif len(v) == 0:
            pass
        else:
            e, B, G, D, A, E = verticalStep(v, e, B, G, D, A, E, True if (iter+1)%noterPerBar==0 else False)
            # actual horizontal manipulating
        iter += 1
    return [e, B, G, D, A, E]

def barFormat(ba):
    return "{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(ba[0], ba[1], ba[2], ba[3], ba[4], ba[5])












## ALL REQUIRED THINGS FOR AUDIO STREAMING


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









opt = open("tab.txt", "a+")
opt.truncate(0)

if __name__ == '__main__':
    for barNotes in mnot.split("\n"):
        b = bar(barNotes)
        opt.write("{0}\n\n\n".format(barFormat(b)))
