"""
Jack Hales, halesyy@gmail.com
Controller (c.py) for splitting up an image,
interacting with iSplitter class.
"""

import sys, os, time
import numpy as np
from PIL import Image
TS = time.time()

sys.path.append(os.path.abspath("../bitmap"))
sys.path.append(os.path.abspath("../tools"))
from Bitmap import *
from Draw import *
from ImageSplitter import *

PilImage = Image.open("test-images/colorfulselfportrait.jpeg")
ImageArr = np.array(PilImage)

iSplit = iSplitter()
iSplit.fromArray(ImageArr).group(top_diff=1.05)
iSplit.saveAllGroups(max=1, endat=-1)

# imageGroups = iSplit.imagifyGroups(max=100, endat=25)
# print(imageGroups)

ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
