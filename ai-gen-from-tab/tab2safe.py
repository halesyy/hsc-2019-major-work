import numpy as np
import random
import math
import json
import re
import itertools
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import collections

# takes in a popualr mono-space tab format and
# steps to generate a E-base-friendly tablature
# that can be compressed and decompressed

conversionClassifier = "! $ % & ' ( ) * + . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ ] ^ _ ` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~ ° ± ² ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾ ¿ À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï  Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý Þ ß"
conversionClassifier = conversionClassifier.split(' ')

# Converting matrix
converter = {}
for conv, i in zip(conversionClassifier, range(0, len(conversionClassifier))):
    converter["{0}".format(conv)] = i
backConverter = {v: k for k, v in converter.items()}

def allEqual(l):
    return np.unique(l).shape[0]<=1

def getTabFromUrl(url):
    request  = Request(url)
    response = urlopen(request)
    html = response.read()
    response.close()
    # Pretifying, then splitting to get tab region as it
    soup = BeautifulSoup(html, features="html.parser")
    phtml = soup.prettify()

    hsplit = phtml.split("***********************************")[0].split(":{\"content\":\"")[1]
    hsplit = hsplit.replace("\\r", "")
    hsplit = hsplit.replace("\\n", "\n")
    hsplit = hsplit.replace("\\\\", "/")
    hsplit = hsplit.replace("\\", "")
    hsplit = hsplit.replace("(", "-")
    hsplit = hsplit.replace(")", "-")
    hsplit = hsplit.replace("h", "-")
    hsplit = hsplit.replace("p", "-")
    hsplit = hsplit.replace("b", "-")
    hsplit = hsplit.replace("/", "-")
    hsplit = hsplit.replace("~", "-")
    hsplit = hsplit.replace("x", "-")

    # print(hsplit)
    return hsplit

def vertical(strings, at):
    return [strings[0][at], strings[1][at], strings[2][at], strings[3][at], strings[4][at], strings[5][at]]

def horizontal(string, weight):
    finalNote = 0
    split = False # whether or not iter is at a split (not int)
    storedNotes = []
    firstStoreLocation = 0
    time = []

    for note, location in zip(string, range(len(string))):

        try:
            note = int(note)
            # SUCCESSFUL INTEGER
            storedNotes.append(note)
            if len(storedNotes) == 1:
                firstStoreLocation = location
            split = False
        except ValueError:
            if split == False:

                # got some serious chugging
                if len(storedNotes) > 2 and allEqual(storedNotes):
                    for c in range(firstStoreLocation, (firstStoreLocation+len(storedNotes))):
                        time.append([c, storedNotes[0]])
                    storedNotes = []
                elif len(storedNotes) == 2:
                    finalNote = (storedNotes[0]*10) + storedNotes[1]
                elif len(storedNotes) == 1:
                    finalNote = storedNotes[0]

                # We have "final_note" which is
                # the final_note value with respect
                # to the weight.
                if len(storedNotes) > 0:
                    finalNote += weight #weight for it's string
                    # print("at {0}, {1} is to be played".format(firstStoreLocation, finalNote))
                    storedNotes = []
                    time.append([firstStoreLocation, finalNote])
            split = True

    # print()
    # print(time)
    return time






tabs = getTabFromUrl("https://tabs.ultimate-guitar.com/tab/megadeth/holy_wars_the_punishment_due_tabs_521861")
t = open("tabs.txt", "w+")
t.write(tabs)
# tabs = open("tabs.txt", "r")
# tabs = tabs.read()


lines = tabs.split("\n")

# First tab is from 0 -> 5
# AFTER 5th iter, we're starting on tab 2 @
# 7 -> 12
# itno = 0
# converter, safe int
safe = "-"*20
safe += "\n"
for line, lineno in zip(lines, range(0, len(lines))):
    #start of a new tabstep
    if len(line) > 0 and line[0] == 'e' and line[1] == '|':
        e, B, G, D, A, E  = lines[lineno], lines[lineno+1], lines[lineno+2], lines[lineno+3], lines[lineno+4], lines[lineno+5]
        # Iterating over each vertical length in an array [0, 1, 2, 3, 4, 5]
        # vert = vertical([e, B, G, D, A, E], 0)
        # vert = vertical([e, B, G, D, A, E], i)
        e, B, G, D, A, E = horizontal(e, 25), horizontal(B, 20), horizontal(G, 15), horizontal(D, 10), horizontal(A, 5), horizontal(E, 0)
        bar = {}
        for i in itertools.chain(*[e, B, G, D, A, E]):
            time = i[0]
            note = backConverter[i[1]]
            # note = str(i[1])
            if time in bar: # the time is already there, so add another note
                bar[int(time)].append(note)
            else:
                bar[int(time)] = [note]

        # bar = collections.OrderedDict(sorted(bar.items()))
        # dict(sorted(bar.items()))
        bar_asc = dict(sorted(bar.items(), key = lambda x:x[0]))
        # print(bar_asc)

        for k in bar_asc:
            # print(k, bar_asc[k])
            safe += ''.join(bar_asc[k])
            safe += ' '
        safe += "" if lineno == len(lines)-1 else "\n"

safe += "-"*20
safe += "\n\n"
print(safe)

















# indvs = tabs.split("\n")
# print(indvs)
