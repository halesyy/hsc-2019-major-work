mnot = """ < 7 2 5
! 92 9 2 4 72 4 4 4 4 7
& 2& 4/& 4/&
A>8 A>8 A>8 A>8 A>8 B>8 C>9 A>8 A>8 A>8 A>8 B>8
A>9 A>8 A>8&
94& 94/ :6/ >84 >84 <84/
A>8 A>8 A>8
> C F
A<74/&
H J H J H J O J
H K H F @ H F C L N
! 1 ! * 4 2 1 ! * 4 2 1 ! * 2 / ! * 2 / : 9 7
9 < 9 7 4 3 0 3 7 3 4 4 3 4 3 1 ; 3 = 8 : 8 < 8 5
5 8 5 5 6 5 1 0 3 5 3
5 * ? < 5 : 5 = : 8 5 . 3
@ C @ B @ > @ ? = > ; ; @ B @
D D D D G L J I J H H G J G D B D B ? = B ID GC B G
:3 ; = = 3 5 8 C? C? =3 . : ; < : 6 < = : ; : = ; :6 5
30 30 30 % % % % ; 8 3 3 8 8 6 3 1
8 : ; : 8 6 8 : ; 6 5 3 1 1 3 8 8 5 5 8 5 9 : 5 < : 5 1 3 5 3 5
1 5 9 5 5 6 1 5 6 8 9 5 6 1 5 8 3 0 1 5 : 5 ; 6 8 : 6 ;6 / C; C ; 0 6 C / C / C B ? / B C B ? 6
! >91 >92 ! =81 ( ! $ ' ( ' ( * + A<6/ 1.2* !
J G J G J H J G F G J G G J G
1* 2+$ 4/)
3* * * * * + * 4+ 3* 4+ 4+ 3* 3( 3* 4+ 3* 4+ & /& .% /& 0' .%
83* % $ % % % % 3.% ! % ( % % % % % 61( 61( 1*!
* 6 W / ( / & /



*! 81 81 . * 81 ( ( ( 3* 3* 3* 3* 4+ 3* 3* 1(
6/ 81 81 81 81 81 * * * * 8/ * * 81 *
;8 9 4 4 1 4 2
61 4/ 4/ 2* 2+ 2+ 41 41 2+ 4/ 2+ 4/ 2+&
4/& 41 84 84 84 94
94+ 94+ 94+ 94+ 94+ 94+ 94+ 1*! 1*! 1! E C 4
=81 ! ! ! 81! ! ! 83* 94+ 94+ 94+ 4/& 4/& 61( 61( 61( 61( 61( 61( 61( 61( 61( 61( 61(
H J H J H F F F H F E F E B E F E B @ = @ M Q M J M O Q R R R R O T R
O M L M L M G M L M L L M L M J H L M O M L



C C C C H C ? C F B C ?951'
5
! >:41+ 3 >:41 >:4 >:41 & ?46 ?84& & & A>94&& & & & A<8& A<84& & & A>9 A;6 A;6
>:41+& @<83.% @<73.% @<83*% ?<72) ??=62+$ ?<6+$ ?<6+$ ?<6+$ ?<6+$
?=60+$ ?=60+$ ?=60+$ ?=60+$ ?=60+$ ?=60+$ ?=60+$
C?9 C?9 A C>9 ?9 C?9 <9 ?9 ?9
A>94+ A>94+ A>94+ A=94+ A=94+ A=94+
4 C? A= C?9 A<94+ A<74+ A<74/& A<74/& A<74/& A<74/& A<74/& A<74/& A<74/& A<74/& A<74/& A<74/& A<74/& A<74/&
( / 2 ( 4/(
F ;6 9 61 94 94 1 / ;61 * * 83 * 83 *
A>8& A>8 A>81 A>8 41 4 > >;61( 6 6 6 9 6
>94& 4 ( 94 ( 94 ( ?6 > 6 4
>:41+ >:41+ >:41+ >:41+ @<6/ @<6/ @<6/ @<6/ A<4/*& A<4/*& A<4/*& A<4/*& A<4/*& @<6/ @<6/
& ( . 1 2 6 : + 1 4 * / 4 & * @<6
"""
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











if __name__ == '__main__':
    for barNotes in mnot.split("\n"):
        b = bar(barNotes)
        print("{0}\n\n\n".format(barFormat(b)))
