"""
Jack Hales, halesyy@gmail.com
The single tie point, meant to make the codebase cleaner and easier to debug. This
is the file combining the 'bitmap' class with the 'draw' class, to create a more rapid
development environment when I begin to develop the robot's mind, being able to quickly
tie in arbritrary libraries and modules in at any point in time.
"""

import sys, os, time, pprint
import numpy as np
from PIL import Image
pp = pprint.PrettyPrinter(indent=4)
pp = pp.pprint
# from multiprocessing import Pool, cpu_count
# from concurrent.futures import ThreadPoolExecutor
TS = time.time()

sys.path.append(os.path.abspath("../bitmap"))
sys.path.append(os.path.abspath("../draw"))
sys.path.append(os.path.abspath("../_breaker"))
from Bitmap import *
from Draw import *
from ImageSplitter import *

Manager = BitmapManager()
Splitter = iSplitter()
# Manager.Template("../bitmap/alphabet-bitmap-ds/k.jpg")\

Manager.Template("../_breaker/test-images/300.jpg")
Manager.Output("position-test") # as

# extracting the colour based splits
im = Manager.Template
arr = np.array(im)
Splitter.fromArray(arr=arr).group(top_diff=1.05)
# top diff closer to 1 means = more diverse pixel range
SplitBitmaps = Splitter.imagifyGroups(max=4, endat=-1)

# print(SplitBitmaps)

for groupx, group in enumerate(SplitBitmaps):
    # print(group)
    colour = group["color"]
    rawimg = group["rawimage"]
    if rawimg == False: continue
    Manager.Template = rawimg
    MapConfig = {
        "by": 15,
        "colour": '#%02x%02x%02x' % (colour[0], colour[1], colour[2]),
        "loose": "low"
    }
    Manager.LoadConfig(MapConfig)
    Manager.InitPixelArray(PixelArray)
    Series = Manager.ExtractSeries()
    Manager.Output("save/{0}".format(groupx))
    Manager.Prep().ApplySeries(Series)
    BitmapDrawn = Manager.GetImage()
    Manager.Save("done")



# MapConfig = {
#     "by":      15,
#     "colour":  [0, 0, 0],
#     "loose":   "medium"
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
# # BitmapDrawn.show()
# Manager.Save("complete").SaveTemplate()


ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
