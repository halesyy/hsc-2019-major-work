"""
Jack Hales, halesyy@gmail.com
The single tie point, meant to make the codebase cleaner and easier to debug. This
is the file combining the 'bitmap' class with the 'draw' class, to create a more rapid
development environment when I begin to develop the robot's mind, being able to quickly
tie in arbritrary libraries and modules in at any point in time.
"""

import sys, os, time, pprint
import numpy as np
import random
from PIL import Image
pp = pprint.PrettyPrinter(indent=4)
pp = pp.pprint
import glob
TS = time.time()
all = glob.glob("memory/*.png")

x, y = Image.open(all[0]).size
canvas = Image.new("RGBA", size=(x, y))

for filename in (all):
    img = Image.open(filename)
    canvas.paste(img, (0, 0), img)

canvas.save("texture-processed.png")
ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
