"""
BREAKS INTO COLOR GROUPS, RE-DRAWS BITMAPS, COMBINES INTO IMAGE.
"""

import sys, os, time, pprint
import numpy as np
from PIL import Image
pp = pprint.PrettyPrinter(indent=4)
pp = pp.pprint
TS = time.time()

sys.path.append(os.path.abspath("../bitmap"))
sys.path.append(os.path.abspath("../tools"))
sys.path.append(os.path.abspath("../_breaker"))
from Bitmap import *
from Draw import *
from ImageSplitter import *

Manager = BitmapManager()
Splitter = iSplitter()
Manager.Template("../_breaker/test-images/200.jpg")
Manager.Output("position-test") # as
from multiprocessing import Pool, cpu_count

# extracting the colour based splits
im = Manager.Template
arr = np.array(im)
Splitter.fromArray(arr=arr).group(top_diff=1.05)
# top diff closer to 1 means = more diverse pixel range
SplitBitmaps = Splitter.imagifyGroups(max=4, endat=-1)

def impact(raw, colour, id):
    Manager.Template = raw
    MapConfig = {
        "by":     40,
        "colour": '#%02x%02x%02x' % (colour[0], colour[1], colour[2]),
        "loose":  'low'
    }
    Manager.LoadConfig(MapConfig)
    Manager.InitPixelArray(PixelArray)
    Series = Manager.ExtractSeries()
    if len(Series) == 0: return False
    # if (len(Series) == 0): print("THIS IS NOT GOOD")
    Manager.Output("save/{0}".format(groupx))
    Manager.Prep().ApplySeries(Series)
    BitmapDrawn = Manager.GetImage()
    Manager.Save("done")

print("Total of {0} groups to sift".format(len(SplitBitmaps)))
for groupx, group in enumerate(SplitBitmaps):
    # if groupx == 5: break
    print("Doing {0}/{1}".format(groupx, len(SplitBitmaps)))
    impact(group["rawimage"], group["color"], groupx)
    # Process(target=impact, args=(group["color"], groupx)).start()

ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
