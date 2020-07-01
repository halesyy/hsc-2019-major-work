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


def impact(groupx, raw, colour, id, sortSquares=True):

    Manager = BitmapManager()
    # inserting the template into it
    Manager.Template = raw
    MapConfig = {
        "by":     80,
        "colour": '#%02x%02x%02x' % (colour[0], colour[1], colour[2]),
        "loose":  'low'
    }

    # getting the series for the piece of data
    Manager.LoadConfig(MapConfig)
    Manager.InitPixelArray(PixelArray)
    Series = Manager.ExtractSeries(sortSquares)
    if len(Series) == 0: return False

    # setting output
    Manager.Output("save/{0}".format(groupx))
    Manager.Prep().ApplySeries(Series)
    BitmapDrawn = Manager.GetImage()

    # combining to main image
    # canvas = Image.open("memory/-1.png") # opening for rexexture processing purposes - blank canvas
    canvas.paste(BitmapDrawn, (0, 0), BitmapDrawn)
    canvas.save("texture-live.png") # saving for live
    # canvas.save("memory/{0}.png".format(groupx)) # saving for retexture processing parse



if __name__ == "__main__":

    Splitter = iSplitter()

    # getting out numpy image from getting
    Manager = BitmapManager()
    Manager.Template("../_breaker/test-images/200.jpg")
    Manager.Output("position-test") # as
    im = Manager.Template

    # numpified, image splitting!
    arr = np.array(im)
    Splitter.fromArray(arr=arr).group(top_diff=1.10)
    SplitBitmaps = Splitter.imagifyGroups(max=20, endat=-1)

    # setting up canvas
    x, y = SplitBitmaps[0]["rawimage"].size
    canvas = Image.new("RGBA", size=(x, y))
    canvas.save("memory/-1.png")

    print("Total of {0} groups to sift".format(len(SplitBitmaps)))
    for groupx, group in enumerate(SplitBitmaps):
        before = time.time()
        print("{0}% - {1}/{2}".format( round(groupx/len(SplitBitmaps)*100, 2), groupx, len(SplitBitmaps) ), end=" ")
        if groupx != -1:
            impact(groupx, group["rawimage"], group["color"], groupx)
            # canvas.save("texture-live.png")
        else:
            Process(target=impact, args=(groupx, group["rawimage"], group["color"], groupx)).start()
        after = time.time()
        print("!: {0} seconds".format(round(after - before, 2)))

ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))

# took 113 on processing, ~50%  decrease
# took 202 on sequential, ~100% increase
