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
from multiprocessing import Pool, Process, cpu_count

def impact(raw, colour, id):
    Manager.Template = raw
    MapConfig = {
        "by":     50,
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





if __name__ == "__main__":
    Manager = BitmapManager()
    Splitter = iSplitter()
    Manager.Template("../_breaker/test-images/200.jpg")
    Manager.Output("position-test") # as

    im = Manager.Template
    arr = np.array(im)
    Splitter.fromArray(arr=arr).group(top_diff=1.03)
    SplitBitmaps = Splitter.imagifyGroups(max=3, endat=-1)

    print("Total of {0} groups to sift".format(len(SplitBitmaps)))
    for groupx, group in enumerate(SplitBitmaps):
        # if groupx == 5: break
        # print("Doing {0}/{1}".format(groupx, len(SplitBitmaps)))
        print("{0}% - {1}/{2}".format( round(groupx/len(SplitBitmaps)*100, 2), groupx, len(SplitBitmaps) ))
        # impact(group["rawimage"], group["color"], groupx)
        Process(target=impact, args=(group["rawimage"], group["color"], groupx)).start()

ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
