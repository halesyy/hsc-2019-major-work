"""
Jack Hales, halesyy@gmail.com
Controller (c.py) for splitting up an image, interacting with iSplitter class.
"""

import sys, os, time
import numpy as np
from PIL import Image
TS = time.time()

sys.path.append(os.path.abspath("../../bitmap"))
sys.path.append(os.path.abspath("../../draw"))
from Bitmap import *
from Draw import *
from ImageSplitter import *

PilImage = Image.open("test-images/200.jpg")
ImageArr = np.array(PilImage)

iSplit = iSplitter()
iSplit.fromArray(ImageArr).groupStart()
iSplit.SaveAllGroups()

ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
