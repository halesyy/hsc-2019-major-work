"""
Jack Hales, halesyy@gmail.com
The single tie point, meant to make the codebase cleaner and easier to debug. This
is the file combining the 'bitmap' class with the 'draw' class, to create a more rapid
development environment when I begin to develop the robot's mind, being able to quickly
tie in arbritrary libraries and modules in at any point in time.
"""

import sys, os, time
# from multiprocessing import Pool, cpu_count
from multiprocessing import Process
TS = time.time()

sys.path.append(os.path.abspath("../bitmap"))
sys.path.append(os.path.abspath("../draw"))
from Bitmap import *
from Draw import *






# Parallel async processing controller pool.
# pool = Pool(processes=60)

def ControllOutput():

    Manager = BitmapManager()
    Manager.Template("../bitmap/alphabet-bitmap-ds/{0}.jpg".format(random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])))
    Manager.Output("position-test")

    #// Configurator
    MapConfig = {
        "by":      16,
        "colour":  "red",
        "loose":   "high"
    }

    Manager.LoadConfig(MapConfig) # a comparable file
    Manager.InitPixelArray(PixelArray) # dep: PixelArray
    Series = Manager.ExtractSeries()

    Manager.Prep().ApplySeries(Series)
    # Manager.Trim()
    Manager.Save("complete").SaveTemplate()

# pool = []


# def p_MANAGE():
    # p = Process(target=ControllOutput)
    # p2 = Process(target=Manager.PA)
    # p1.start()
    # p2.start()
    # pool.append(p1)
#

# for i in range(60): p_MANAGE()
[Process(target=ControllOutput).start() for x in range(60)]


ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
