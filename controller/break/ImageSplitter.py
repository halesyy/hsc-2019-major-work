"""
Role of this class:

1. Input an original image
2. Split into dominant colours/ group the sections
   - Start from random X/Y point
   - Start going out in UDLR patten till meeting a colour which is not under 20% diff
   - Once the entire collection recurs and collapses, cache that as a "group" and
     delete it from the "choosing" record and find a new place to start prying around for
     the colours.
   - This leaves a bunch of groups and automatically removes itself from the array
     meaning it cannot be chosen again.
   - Once there are no more pixels, we're good to convert all "groups" into bitmaps.
3. Large collection of Bitmaps with appropriate XY placement locations
4. Render all bitmaps and place into the new image
"""

import pprint as pprint
pp = pprint.PrettyPrinter(indent=4)
pp = pp.pprint
import random

class iSplitter:
    def __init__(self):
        self.Groups = []
        pass

    def fromArray(self, arr):
        self.ImgArr = arr
        self.Width = arr.shape[1]  # these are whole, counting from 1->tot, not 0
        self.Height = arr.shape[0] # . . . . . . . .

    def SortColors(self):
        colours = {}
        self.Cache = []
        y, x = 0, 0
        for yrow in self.ImgArr:
            x = 0
            self.Cache.append([])
            for xcolours in yrow:
                hex = '#%02x%02x%02x' % (xcolours[0], xcolours[1], xcolours[2])
                if hex in colours.keys(): colours[hex] += 1
                else: colours[hex] = 1
                self.Cache[y].append([])
                self.Cache[y][x] = xcolours
                x += 1
            y += 1
        self.XRange = x
        self.YRange = y
        self.Colours = colours

    def GroupStart(self):
        # group = []
        xr, yr = random.randint(0, self.XRange), random.randint(0, self.YRange)
        self.GroupFrom(xr, yr)

        # print(self.Width, self.Height)
        # print(group)
        # print("{0} {1} {2}".format((parent_col[0]*diff_range_up), (parent_col[1]*diff_range_up), (parent_col[2]*diff_range_up)))
        # print("{0} {1} {2}".format((parent_col[0]*diff_range_down), (parent_col[1]*diff_range_down), (parent_col[2]*diff_range_down)))
        # print(parent_col)

    def GroupFrom(x, y):
        
        parent_col = self.Cache[y][x]

        diff_range_up   = 1.20 # 20% difference allowed
        diff_range_down = 2 - diff_range_up

        #app+delete
        group.append([yr, xr, parent_col])
        del self.Cache[yr][xr]
        print(self.Width)
        Movements = {
            "U": [xr, yr-(self.Width-1)],
            "D": [xr, yr+(self.Width-1)],
            "L": [xr-1, yr],
            "R": [xr+1, yr],
        }

        print(xr, yr)
        pp(Movements)
