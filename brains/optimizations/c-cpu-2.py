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
Manager = BitmapManager()

def ControllOutput():
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




# Parallel async processing controller pool.
# pool = Pool(processes=60)
if __name__ == "__main__":
    procs = []
    for x in range(60):
        p = Process(target=ControllOutput)
        p.start()
        # procs.append(p)
        # p.join()
    for process in procs:
        process.join()

    ES = time.time()
    print("\ntime to execute: {0}".format(ES - TS))
