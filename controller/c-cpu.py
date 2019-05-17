"""
Jack Hales, halesyy@gmail.com
The single tie point, meant to make the codebase cleaner and easier to debug. This
is the file combining the 'bitmap' class with the 'draw' class, to create a more rapid
development environment when I begin to develop the robot's mind, being able to quickly
tie in arbritrary libraries and modules in at any point in time.
"""

import sys, os, time
from multiprocessing import Pool, cpu_count
# from concurrent.futures import ThreadPoolExecutor
TS = time.time()

sys.path.append(os.path.abspath("../bitmap"))
sys.path.append(os.path.abspath("../draw"))
from Bitmap import *
from Draw import *

Manager = BitmapManager()
Manager.Template("../bitmap/alphabet-bitmap-ds/k.jpg")
Manager.Output("position-test")

#// Configurator
MapConfig = {
    "by":      16,
    "colour":  "random",
    "loose":   "high"
}

Manager.LoadConfig(MapConfig) # a comparable file
Manager.InitPixelArray(PixelArray) # dep: PixelArray

# Parallel async processing controller pool.
pool = Pool(processes=60)

# Series is the path data that can be used
# in Draw to draw over a blank canvas.
for i in range(60):
    pool.apply_async(Manager.ExtractSeries)
    # pool.apply_async(Manager.PA)

pool.close()
pool.join()

# Preparing a new canvas for us to plaster over.
# Manager.Prep().ApplySeries(Series)
# Manager.Trim()
# Manager.Save("complete").SaveTemplate()

ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
