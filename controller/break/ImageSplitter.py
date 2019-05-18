"""
Role of this class:

1. Input an original image
2. Split into dominant colours/ group the sections
3. Large collection of Bitmaps with appropriate XY placement locations
4. Render all bitmaps and place into the new image
"""

import pprint as pprint
pp = pprint.PrettyPrinter(indent=4)
pp = pp.pprint

class iSplitter:
    def __init__(self):
        pass

    def fromArray(self, arr):
        self.ImgArr = arr

    def SortColors(self):
        colours = {}
        y, x = 0, 0
        for yrow in self.ImgArr:
            x = 0
            for xcolours in yrow:
                hex = '#%02x%02x%02x' % (xcolours[0], xcolours[1], xcolours[2])
                if hex in colours.keys(): colours[hex] += 1
                else: colours[hex] = 1
                x += 1
            y += 1
        self.Colours = colours
