"""
Jack Hales, halesyy@gmail.com
The single tie point, meant to make the codebase cleaner and easier to debug. This
is the file combining the 'bitmap' class with the 'draw' class, to create a more rapid
development environment when I begin to develop the robot's mind, being able to quickly
tie in arbritrary libraries and modules in at any point in time.
"""

if __name__ == "__main__":

    # IMPORTING LIBRARIES AND STARTING TIMER
    import sys, os, time
    TS = time.time()
    from multiprocessing import Pool, cpu_count
    sys.path.append(os.path.abspath("../bitmap"))
    sys.path.append(os.path.abspath("../draw"))
    from Bitmap import *
    from Draw import *

    Manager = BitmapManager()
    Manager.Template("../bitmap/alphabet-bitmap-ds/k.jpg")
    Manager.Output("position-test")

    MapConfig = { #conf
        "by":      16,
        "colour":  "random",
        "loose":   "high"
    }

    Manager.LoadConfig(MapConfig) # a comparable file
    Manager.InitPixelArray(PixelArray) # dep: PixelArray

    pool = Pool(processes=1)
    for i in range(60):
        pool.apply_async(Manager.ExtractSeries)

    pool.close()
    pool.join() #60% of time used
    ES = time.time()
    print("\nTime to execute: {0} seconds".format(round(ES - TS, 2)))
