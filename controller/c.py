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
import pprint as pprint
from Bitmap import *
from Draw import *
pp = pprint.PrettyPrinter(indent=4)
pp = pp.pprint

Manager = BitmapManager()
Manager.Template("../bitmap/alphabet-bitmap-ds/a.jpg")
Manager.Output("alpha-test")
# Series is the path data that can be used
# in Draw to draw over a blank canvas.
Series = Manager.ExtractSeries(PixelArray)
# Series = [
#     [0, 0, 135, [0,32,0,32], 0, "BR"]
# ]
# pp(Series)
Manager.PA.TestBounds()

# Preparing a new canvas for us to plaster over.
Manager.Prep().ApplySeries(Series)
# Manager.Trim()
Manager.Save("tdone").SaveTemplate()
