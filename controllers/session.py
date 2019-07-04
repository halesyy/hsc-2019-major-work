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
Manager.Template("../_breaker/test-images/300.jpg")
Manager.Output("position-test") # as
from multiprocessing import Pool, cpu_count

# extracting the colour based splits
im = Manager.Template
arr = np.array(im)
Splitter.fromArray(arr=arr).group(top_diff=1.5)
# top diff closer to 1 means = more diverse pixel range
SplitBitmaps = Splitter.imagifyGroups(max=4, endat=-1)


def impact(raw, colour, id):
    Manager.Template = raw
    MapConfig = {
        "by":     20,
        "colour": '#%02x%02x%02x' % (colour[0], colour[1], colour[2]),
        "loose":  'medium'
    }
    Manager.LoadConfig(MapConfig)
    Manager.InitPixelArray(PixelArray)
    Series = Manager.ExtractSeries()
    Manager.Output("save/{0}".format(groupx))
    Manager.Prep().ApplySeries(Series)
    BitmapDrawn = Manager.GetImage()
    Manager.Save("done")

# pool = Pool(processes=4)

print("Total of {0} groups to sift".format(len(SplitBitmaps)))
for groupx, group in enumerate(SplitBitmaps):
    print("Doing {0}/{1}".format(groupx, len(SplitBitmaps)))
    impact(group["rawimage"], group["color"], groupx)

# [Process(target=impact, args=(group["rawimage"], group["color"], groupx)).start() for groupx, group in enumerate(SplitBitmaps)]
# pool.close()
# pool.join()

# if __name__ == "__main__":

    # for groupx, group in enumerate(SplitBitmaps):
        # if groupx == 10: break
        # colour, raw = group["color"], group["rawimage"]
        # impact(raw, colour, groupx)
        # p = Process(target=impact, args=(raw, colour, groupx))
        # p.start()
        # pool.apply_async(impact, args=(raw, colour, groupx)).get()

    # pool.close()
    # pool.join()

        # Manager.Template = raw
        # MapConfig = {
        #     "by":     20,
        #     "colour": '#%02x%02x%02x' % (colour[0], colour[1], colour[2]),
        #     "loose":  'low'
        # }
        # Manager.LoadConfig(MapConfig)
        # Manager.InitPixelArray(PixelArray)
        # Series = Manager.ExtractSeries()
        # Manager.Output("save/{0}".format(groupx))
        # Manager.Prep().ApplySeries(Series)
        # BitmapDrawn = Manager.GetImage()
        # Manager.Save("done")


# ES = time.time()
# print("\ntime to execute: {0}".format(ES - TS))
