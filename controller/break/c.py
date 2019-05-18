"""
Jack Hales, halesyy@gmail.com
The single tie point, meant to make the codebase cleaner and easier to debug. This
is the file combining the 'bitmap' class with the 'draw' class, to create a more rapid
development environment when I begin to develop the robot's mind, being able to quickly
tie in arbritrary libraries and modules in at any point in time.
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

PilImage = Image.open("test-images/koci.jpg")
ImageArr = np.array(PilImage)

iSplit = iSplitter()
iSplit.fromArray(ImageArr)
iSplit.SortColors()
iSplit.GroupStart()

# Manager = BitmapManager()
# Manager.Template("../../bitmap/alphabet-bitmap-ds/k.jpg")
# Manager.Output("position-test")
#
# #conf
# MapConfig = {
#     "by":      16,
#     "colour":  "random",
#     "loose":   "high"
# }
#
# # conf.load
# Manager.LoadConfig(MapConfig) # a comparable file
# Manager.InitPixelArray(PixelArray) # dep: PixelArray
# Series = Manager.ExtractSeries()
# Parr = Manager.PA
#
# #conf.save
# Manager.Prep().ApplySeries(Series)
# BitmapDrawn = Manager.GetImage()
# BitmapDrawn.show()


ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
