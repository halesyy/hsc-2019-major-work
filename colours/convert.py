from PIL import Image, ImageDraw
import numpy as np
import random, time, math, textwrap

convert = "jack smells like rotten eggs"

converted = Image.new("RGB", [len(convert), 1])
# nparray   = np.array(converted)

colours = {
    "a": "amber",
    "e": "emerald",
    "i": "ivory",
    "o": "orange",
    "u": "ultramarine" ,
    "b": "blue",
    "c": "crimson",
    "d": "denim",
    "f": "fuchsia",
    "g": "gold",
    "h": "hollywood",
    "j": "jade",
    "k": "khaki",
    "l": "lemon",
    "m": "magenta",
    "n": "navy blue",
    "p": "purple",
    "q": "quartz",
    "r": "red",
    "s": "salmon",
    "t": "turquoise",
    "v": "violet",
    "w": "wisteria",
    "x": "xanthic",
    "y": "yellow",
    "z": "zucchini",
    " ": " "
}

# def ColourPixelAt(x, y, width, colour):
#     draw.rectangle([(x, y), (x+width,y +width)], colour)
#
# print(nparray)
print("\n\n")
for i, letter in enumerate(convert):
    print(colours[letter], end=" ")
print("\n\n")
<<<<<<< HEAD

# im = Image.fromarray(nparray)
# im.save("con.jpg")
=======
# im = Image.fromarray(nparray)
# im.save("con.png")
>>>>>>> 0799cf1938fe181db09926fec362ec7bf1c7e999
