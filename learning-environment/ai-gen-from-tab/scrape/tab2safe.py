# coding=utf-8

import numpy as np
import random
import math
import json
import re
import codecs
import itertools
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import collections
from multiprocessing import Process

# takes in a popualr mono-space tab format and
# steps to generate a E-base-friendly tablature
# that can be compressed and decompressed

conversionClassifier = u"! $ % & ' ( ) * + . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ ] ^ _ ` a b c d e f g h i j k l m n o p q r s t u v w x y z { } ~ ° ± ² ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾ ¿ À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý Þ ß"
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

    openingSplit = phtml.split("window.UGAPP.store.i18n")
    # print(len(openingSplit))
    if len(openingSplit) == 1: return False

    hsplit = openingSplit[0].split("window.UGAPP.store.page")[1]
    # hsplit = hsplit.replace("r", "")
    hsplit = hsplit.replace("\\n", "\n")
    hsplit = hsplit.replace("\\\\", "/")
    hsplit = hsplit.replace("\\", "")
    hsplit = hsplit.replace("(", "-")
    hsplit = hsplit.replace(")", "-")
    hsplit = hsplit.replace("h", "-")
    hsplit = hsplit.replace("p", "-")
    hsplit = hsplit.replace("b", "-")
    hsplit = hsplit.replace("r", "-")
    hsplit = hsplit.replace("t", "-")
    hsplit = hsplit.replace("/", "-")
    hsplit = hsplit.replace("~", "-")
    hsplit = hsplit.replace("x", "-")
    hsplit = hsplit.replace("'", "-")
    hsplit = hsplit.replace("`", "-")
    hsplit = hsplit.replace("^", "-")
    hsplit = hsplit.replace(">", "-")
    hsplit = hsplit.replace("<", "-")

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
    specials = ['|']

    # Iterating each character in the string (which is a length)
    # of a string on the bar.
    for note, location in zip(string, range(len(string))):

        # Doing checks for specials, e.g. bars or other chars
        if note in specials:
            # storedNotes.append()
            # RECENTS_SPECIAL is NOT the current NOTE
            time.append([location, note])

        # Is a simple character
        else:
            try:
                # Checking if the note is an integer, to try to impart it
                note = int(note)
                storedNotes.append(note)
                if len(storedNotes) == 1: firstStoreLocation = location
                split = False
                # recentSpecial = None

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

                        storedNotes = []
                        time.append([firstStoreLocation, finalNote])
                split = True
    return time




def pipeSafeFromUrl(url):
    tab_data = getTabFromUrl(url)
    if tab_data == False: return False
    lines = tab_data.split("\n")
    if len(lines) < 10: return False

    safe = "\n"
    # safe += "-"*30
    # safe += "\n"

    # Each individual line of the content
    # file.
    for line, lineno in zip(lines, range(0, len(lines))):

        # Noticing that there is an "e",
        # followed by "|" to start the parse.
        if len(line) > 0 and line[0] == 'e' and line[1] == '|':
            e, B, G, D, A, E = lines[lineno], lines[lineno+1], lines[lineno+2], lines[lineno+3], lines[lineno+4], lines[lineno+5]
            # Iterating over each vertical length in an array [0, 1, 2, 3, 4, 5]
            e, B, G, D, A, E = horizontal(e, 25), horizontal(B, 20), horizontal(G, 15), horizontal(D, 10), horizontal(A, 5), horizontal(E, 0)

            # Starting a new bar, and iterating in parallel
            bar = {}
            for i in itertools.chain(*[e, B, G, D, A, E]):

                # The starting location

                time = i[0]
                fret = i[1]

                if fret == '|': # Special character
                    note = '|'
                else: # Normal fret note @ time
                    note = backConverter[fret]

                # Time exists, append to the current bar at time
                if time in bar: bar[int(time)].append(note)
                else: bar[int(time)] = [note]

            # Sorting from the lower notes
            bar_asc = dict(sorted(bar.items(), key = lambda x:x[0]))

            for k in bar_asc:
                # print(k, bar_asc[k])
                safe += ''.join(bar_asc[k])
                safe += ' '

            safe += "" if lineno == len(lines)-1 else "\n"

    safe = re.sub('\|+', '|', safe)
    if len(lines) < 5: return ""
    return safe




def PARALLEL_pipeSafeFromUrl(link, no):
    safef = codecs.open("safedump.txt", "a+", "utf8")
    safe  = pipeSafeFromUrl(link)
    if safe == False:
        errorf = codecs.open("error.txt", "a+", "utf8")
        errorf.write(link+"\n")
        print("{0}: Failed {1}, saved to error.txt".format(no, link))
    else:
        safef.write(safe)
        print("{0}: Finished {1} successfully".format(no, link))




def filterForArtistOrTab(urlset):
    filteredUrls = []
    for url in urlset:
        spl = url.split("/")

        if "power" in url or "video" in url or "pro" in url:
            pass
        elif len(spl) > 3 and spl[3] == 'tab':
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
    # dsf.truncate(0)
    urlsFromDS = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ds)
    filteredUrls = filterForArtistOrTab(urlsFromDS)
    return filteredUrls




def DumpLinksToSafe(links, len=-1):
    ps, iter = [], 0

    for link in links:
        if len == iter: break
        p = Process(target=PARALLEL_pipeSafeFromUrl, args=[link, iter])
        p.start()
        time.sleep(0.25)
        iter += 1
    for p in ps:
        p.join()


        # safe = PARALLEL_pipeSafeFromUrl(link)

if __name__ == '__main__':
    ALINKS = ArtistLinks()
    print("ABOUT TO PROCESS {0} LINKS... WARNING!".format(len(ALINKS)))
    print(pipeSafeFromUrl("https://tabs.ultimate-guitar.com/tab/metallica/nothing_else_matters_tabs_8519"))
    # DumpLinksToSafe(ALINKS)

# s = pipeSafeFromUrl("https://tabs.ultimate-guitar.com/tab/lessons_-_scales/major_scales_tabs_160615")
# print(s)
