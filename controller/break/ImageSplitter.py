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
        self.CurrentLCIndex = 0
        pass

    def fromArray(self, arr):
        self.ImgArr = arr
        self.ContainedImage = Image.fromarray(arr)
        self.Width = arr.shape[1]  # these are whole, counting from 1->tot, not 0
        self.Height = arr.shape[0] # . . . . . . . .
        self.W = arr.shape[1]
        self.H = arr.shape[0]
        return self.SortColors()

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
        return self












    def CreateImageFromGroup(self, groupid, max=False):
        group = self.Groups[groupid]
        if max != False and len(group) < max: return False
        img = Image.new("RGB", (self.Width, self.Height), "black")
        imgarr = np.array(img)
        contained = np.array(self.ContainedImage)
        for xy in group:
            x, y = xy # the x/y coords in self.Cache
            colorcache = contained[y][x]
            imgarr[y][x] = colorcache
        img = Image.fromarray(imgarr)
        return img




    def saveAllGroups(self, max=50):
        for gid, group in enumerate(self.Groups):
            saveas = "split-groups/{0}.jpg".format(gid)
            image  = self.CreateImageFromGroup(gid, max=max)
            if image == False: continue
            image.save(saveas)



    #/\/ Moves through the location cache
    #/\/ efficiently.
    #/\/ Managing from self.CurrentLCIndex
    def GetLocationCacheNext(self):
        newValueToCreep = False
        for i in range(self.CurrentLCIndex, len(self.LocationCache)):
            if self.LocationCache[i] == "":
                # continue exec till finding it
                continue
            else:
                # we just found it, return and remove
                self.CurrentLCIndex = i
                newValueToCreep = self.LocationCache[i]
                self.LocationCache[i] = ""
                break
        # print("returning {0}".format(newValueToCreep))
        return newValueToCreep




    def group(self):
        creepLocationString = self.GetLocationCacheNext()
        xr, yr = map(int, creepLocationString.split(":"))
        self.CurrentGroup = 0
        self.Groups.append([]) #store

        toExpand = ["{0}:{1}".format(xr, yr)]
        pixel = self.Cache[yr][xr]
        r,g,b = pixel

        top_diff    = 1.45            # 20% over
        bottom_diff = 2.00 - top_diff # 20% under

        iters = 0

        while len(self.LocationCache) != 0:

            iters += 1
            # print("at iter {0}, len: {1}".format(iters, len(toExpand)))

            if len(toExpand) == 0:
                # print("Going to create a new group")

                creepLocationString = self.GetLocationCacheNext()
                if creepLocationString == False:
                    break

                xr, yr = map(int, creepLocationString.split(":"))
                toExpand = ["{0}:{1}".format(xr, yr)]
                pixel = self.Cache[yr][xr]
                r,g,b = pixel
                #g+1
                self.CurrentGroup += 1
                self.Groups.append([])
                print(self.CurrentGroup, end=", ")

            #/\/

            expanding = toExpand.pop(0)
            # print("for exand {0}".format(expanding))
            # print(toExpand)
            x, y = [int(x) for x in expanding.split(":")]
            if self.RemoveFromLocationCacheAndSave(x, y) == False: continue
            Movements = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]] #udlr
            Movements = filter(lambda v: False if (v[0]<0 or v[0]>=self.W) or (v[1]<0 or v[1]>=self.H) else True, Movements)


            for xy in Movements:
                xmove, ymove = xy

                try:
                    nr,ng,nb = self.Cache[ymove][xmove]
                except IndexError:
                    continue

                if (self.LocationCache[(ymove*(self.Width))+xmove] == "") or (self.Cache[ymove][xmove][0] == -1) or ((nr >= r*top_diff) or (ng >= g*top_diff) or (nb >= b*top_diff) or (nr <= r*bottom_diff) or (ng <= g*bottom_diff) or (nb <= b*bottom_diff)):
                    continue
                else:
                    toExpand.append("{0}:{1}".format(xmove, ymove))

        print("Took a total of {0} iterations...".format(iters))





    def RemoveFromLocationCacheAndSave(self, x, y):
        # toRemove = "{0}:{1}".format(x, y)
        # if toRemove not in self.LocationCache: return False

        try:
            # del self.LocationCache[(y*self.Width) + x]
            # print("Removing {0}:{1}".format(x, y))
            # print("Removing {0}".format(toRemove))
            # xt,yt = map(int, toRemove.split(":"))
            self.LocationCache[(y*(self.Width)) + x] = ""
            # self.LocationCache.remove(toRemove)
            # 1. iterate and keep a cache internally for
            #    the current iteation through locationcache from 0->onwards,
            # 2. simply access and set to = "" using above, then
            #    when getting a new one simply start iterating from left
            #    to right, self caching the current index then moving
            #    there and keep moving from left right till you find the next


            self.Cache[y][x][0] = -1
            self.Groups[self.CurrentGroup].append([x, y]) #can get self.Cache[y][x]
            return True

        except IndexError or ValueError:
            return False

        return True
