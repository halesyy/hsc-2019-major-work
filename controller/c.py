"""
Jack Hales, halesyy@gmail.com
The single tie point, meant to make the codebase cleaner and easier to debug. This
is the file combining the 'bitmap' class with the 'draw' class, to create a more rapid
development environment when I begin to develop the robot's mind, being able to quickly
tie in arbritrary libraries and modules in at any point in time.
"""

import sys, os

sys.path.append(os.path.abspath("../bitmap"))
sys.path.append(os.path.abspath("../draw"))
from Bitmap import *
from Draw import *

Manager = BitmapManager()
Manager.Template("../bitmap/alphabet-bitmap-ds/a.jpg")
Manager.Output("position-test")

MapConfig = {
    "by":      32,
    "colour":  "#f44336",
    "loose":   "medium"
}

Manager.LoadConfig(MapConfig) # a comparable file
Manager.InitPixelArray(PixelArray) # dep: PixelArray

# Series is the path data that can be used
# in Draw to draw over a blank canvas.
Series = Manager.ExtractSeries()
Parr = Manager.PA

# Preparing a new canvas for us to plaster over.
Manager.Prep().ApplySeries(Series)
# Manager.Trim()
Manager.Save("complete").SaveTemplate()
