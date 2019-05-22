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
from PIL import Image, ImageDraw
import random, sys
import numpy as np
# sys.setrecursionlimit(300000) # doing a lot...

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
        self.LocationCache = []
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
                self.LocationCache.append("{0}:{1}".format(x, y)) # x/y
                x += 1
            y += 1
        self.XRange = x
        self.YRange = y
        self.Colours = colours












    def CreateImageFromGroup(self, groupid):
        group = self.Groups[groupid]
        img = Image.new("RGB", (self.Width, self.Height), "black")
        imgarr = np.array(img)
        print(group)
        for xy in group:
            x, y = xy # the x/y coords in self.Cache
            print(x, y)
            colorcache = self.Cache[y][x]
            imgarr[y][x] = colorcache
        img = Image.fromarray(imgarr)
        return img
        # img.show()







    def DisplayGroupSize(self):
        for i, groupArray in enumerate(self.Groups):
            print("{0}: {1} length".format(i, len(groupArray)))

    def SaveAllGroups(self):
        for gid, group in enumerate(self.Groups):
            saveas = "split-groups/{0}.jpg".format(gid)
            image  = self.CreateImageFromGroup(gid)
            image.save(saveas)





    def GroupStart(self):
        xr, yr = random.choice(self.LocationCache).split(":")
        xr, yr = int(xr), int(yr)
        print(xr, yr)

        self.CurrentGroup = 0
        self.Groups.append([]) #store

        toExpand = ["{0}:{1}".format(xr, yr)]
        pixel = self.Cache[yr][xr]
        r,g,b = pixel

        top_diff    = 1.20            # 20% over
        bottom_diff = 2.00 - top_diff # 20% under

        lastAm = len(self.LocationCache)
        sameAmountFor = 0

        while len(self.LocationCache) != 0:

            # print("g... group {0} - len {1}, has been same for: {2}".format(self.CurrentGroup, lastAm, sameAmountFor))
            # print(toExpand)
            # input("...")
            print(len(self.LocationCache))
            input("...")

            if sameAmountFor >= 5: # managing more than 5
                xr, yr = random.choice(self.LocationCache).split(":")
                xr, yr = int(xr), int(yr)

                toExpand = ["{0}:{1}".format(xr, yr)]
                pixel = self.Cache[yr][xr]
                r,g,b = pixel
                sameAmountFor = 0

                self.CurrentGroup += 1
                self.Groups.append([]) #store
                print("Changing group, 5 iterations in a row. New: {0}".format(self.CurrentGroup))

            sameAmountFor = sameAmountFor + 1 if len(self.LocationCache) == lastAm else 0
            lastAm = len(self.LocationCache)

            for i, expand in enumerate(toExpand):
                # print(expand)
                x, y = expand.split(":")
                x, y = int(x), int(y)
                toExpand.remove(expand)
                if self.RemoveFromLocationCacheAndSave(x, y) == False: continue

                # Iterating over movements to see if applicable to next 4 adjacent squares to current expanding
                Movements = {
                    "U": [x, y-1],
                    "D": [x, y+1],
                    "L": [x-1, y],
                    "R": [x+1, y],
                }
                for move, to in Movements.items():
                    xset, yset = to
                    if xset < 0 or xset > self.Width or yset < 0 or yset > self.Height: continue
                    try: # catching any indexing errors cause of the nature of this call
                        nr,ng,nb = self.Cache[yset][xset]
                    except IndexError: continue

                    if self.Cache[yset][xset][0] == -1 or (
                        # for ignoring
                        (nr >= r*top_diff)      or    (ng >= g*top_diff)      or    (nb >= b*top_diff)      or
                        (nr <= r*bottom_diff)   or    (ng <= g*bottom_diff)   or    (nb <= b*bottom_diff)
                    ):
                        continue
                    else:
                        toExpand.append("{0}:{1}".format(xset,yset))

            # toExpand = []







    def RemoveFromLocationCacheAndSave(self, x, y):
        toRemove = "{0}:{1}".format(x, y)
        if toRemove not in self.LocationCache: return False

        try:
            # del self.LocationCache[(y*self.Width) + x]
            # print("Removing {0}:{1}".format(x, y))
            self.LocationCache.remove(toRemove)
            self.Cache[y][x][0] = -1
            self.Groups[self.CurrentGroup].append([x, y]) #can get self.Cache[y][x]
            # print("True")
            return True
        except IndexError or ValueError:
            # print("Oops, index is out! {0},{1}: {2}".format(x, y, (x*self.Width) + x))
            # print("False")
            return False
        # return True






    def GroupFrom(self, x, y):
        currentgroup = self.CurrentGroup
        parent_col = self.Cache[y][x]

        diff_range_up   = 1.20 # 20% difference allowed
        diff_range_down = 2 - diff_range_up

        #app+delete
        self.Groups[currentgroup].append([y, x, parent_col])
        self.Cache[y][x] = [-1, -1, -1]

        Movements = {
            "U": [x, y-1],
            "D": [x, y+1],
            "L": [x-1, y],
            "R": [x+1, y],
        }

        for movement, xy in Movements.items():
            # print(movement, xy)
            nx, ny = xy
            if (nx >= 0 and nx < self.Width) and (ny >= 0 and ny < self.Height) and self.Cache[ny][nx][0] != -1:
                self.GroupFrom(nx, ny)
