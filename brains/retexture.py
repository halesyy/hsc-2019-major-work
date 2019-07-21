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
# from multiprocessing import Pool, cpu_count
# from concurrent.futures import ThreadPoolExecutor
import glob
TS = time.time()
all = glob.glob("save/*.png")

x, y = Image.open(all[0]).size
canvas = Image.new("RGBA", size=(x, y))

# basically, this is just:
# creating a canvas from the first image in the set
# pasting from the furthest number to the closest number
# thats about it really
# for i in range(len(all)*3):
#     filename = random.choice(all)
#     img = Image.open(filename)
#     canvas.paste(img, (0, 0), img)

for filename in (all):
    img = Image.open(filename)
    canvas.paste(img, (0, 0), img)

canvas.save("texture.png")
ES = time.time()
print("\ntime to execute: {0}".format(ES - TS))
