import numpy as np
import random
import math
import json
import re
import itertools
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import collections
from multiprocessing import Process

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



# simple function
def rhtml(url):
    request  = Request(url)
    response = urlopen(request)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, features="html.parser")
    phtml = soup.prettify()
    return phtml




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
    return time




def pipeSafeFromUrl(url):
    tab_data = getTabFromUrl(url)
    lines = tab_data.split("\n")

    safe = "\n"
    safe += "-"*30
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
            bar_asc = dict(sorted(bar.items(), key = lambda x:x[0]))
            for k in bar_asc:
                # print(k, bar_asc[k])
                safe += ''.join(bar_asc[k])
                safe += ' '
            safe += "" if lineno == len(lines)-1 else "\n"
    if len(lines) < 5: return ""
    return safe

def PARALLEL_pipeSafeFromUrl(link):
    safef = open("safedump.txt", "a+")
    safe  = pipeSafeFromUrl(link)
    print("Finished {0}!\n".format(link))
    safef.write(safe)

def filterForArtistOrTab(urlset):
    filteredUrls = []
    for url in urlset:
        spl = url.split("/")
        # print(spl)
        if len(spl) > 3 and spl[3] == 'tab':
            filteredUrls.append(url)
        elif len(spl) > 3 and spl[3] == 'artist':
            filteredUrls.append(url)
    return filteredUrls


# Iterates through each set of links presented to the bare content,
# and finds links inside of those links, creating a large array of links
# So far, we've processed: Metallica, Iron Maiden, Queen, Bach (classical), Classical artiss,
# Deep Purple,
def ArtistLinks():
    dsf = open("contentset.txt", "r+", encoding="utf8")
    ds  = dsf.read()
    dsf.truncate(0)
    urlsFromDS = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ds)
    filteredUrls = filterForArtistOrTab(urlsFromDS)
    return filteredUrls

def DumpLinksToSafe(links):
    ps = []
    for link in links:
        p = Process(target=PARALLEL_pipeSafeFromUrl, args=[link])
        p.start()
    for p in ps:
        p.join()

        # safe = PARALLEL_pipeSafeFromUrl(link)

if __name__ == '__main__':
    ALINKS = ArtistLinks()
    print("ABOUT TO PROCESS {0} LINKS... WARNING!".format(len(ALINKS)))
    DumpLinksToSafe(ALINKS)
