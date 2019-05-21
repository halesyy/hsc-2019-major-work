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
import random, sys
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
                self.LocationCache.append([x, y]) # x/y
                x += 1
            y += 1
        self.XRange = x
        self.YRange = y
        self.Colours = colours

    def RemoveFromLocationCacheAndSave(self, x, y):
        try:
            del self.LocationCache[(y*self.Width) + x]
            self.Cache[y][x][0] = -1
            self.Groups[self.CurrentGroup] = self.Cache[y][x]
            return True
        except IndexError:
            # print("Oops, index is out! {0},{1}: {2}".format(x, y, (x*self.Width) + x))
            return False
        # return True

    def GroupStart(self):
        # 1. iterating over
        # meta-array  in  charge  for  random choices,  basically  when  doing the
        # color iteration, cache that xy data into a 2D array that can be randomly
        # chosen  then once it's used  in the  itertions, convert  the inside  X/Y
        # into the index using the  X*Ywid+X 2d->1d  indexing algorithm and delete
        # it so that the cache is removed
        # iterate  by  the  meta  array's length  and as it goes  down  it's  good
        # basically we're creating an abstraction layer that is abstractly
        # interfering and copying data to group it by the colour and locationtype.
        # the advantage is that we can simply start the grouping process from randomly
        # choosing from one as the parent controller.
        xr, yr = random.choice(self.LocationCache)
        # xr, yr = 0, 0
        self.CurrentGroup = 0
        self.Groups.append([]) #store
        toExpand = [[xr, yr]]
        pixel = self.Cache[yr][xr]
        r,g,b = pixel

        top_diff    = 1.2 # 20% over
        bottom_diff = 2 - top_diff # 20% under
        lastAm = len(self.LocationCache)
        sameAmountFor = 0

        while len(self.LocationCache) != 0:
            if lastAm == 4:
                lastAm = 0
                xr, yr = random.choice(self.LocationCache)
                self.CurrentGroup += 1
                print("Changed group...")
                
            for expand in toExpand:

                x, y = expand
                x, y = int(x), int(y)
                # Remove from the LocData + Cache, if False means that it failed to remove
                # because of an indexing error in both. - Ignore the tuple
                if self.RemoveFromLocationCacheAndSave(x, y) == False:
                    continue
                Movements = {
                    "U": [x, y-1],
                    "D": [x, y+1],
                    "L": [x-1, y],
                    "R": [x+1, y],
                }

                # checking for the same # amt since last loop
                if len(self.LocationCache) == lastAm:
                    sameAmountFor += 1
                else: sameAmountFor = 0

                for move, to in Movements.items():
                    xset, yset = to
                    if xset < 0 or yset < 0: continue
                    self.Cache[yset][xset][0] = -1
                    # print(len(self.LocationCache))
                    # IMPORTANT Doing the check to either continue adding 4 or to stop at this node.
                    # 1. New movement area is set to -1, ignore!, 2. New pixel is over or under the threshold for continuing
                    nr,ng,nb = self.Cache[yset][xset]
                    if self.Cache[yset][xset][0] == -1 or (
                        # for ignoring
                        (nr >= r*top_diff)      or
                        (ng >= g*top_diff)      or
                        (nb >= b*top_diff)      or
                        (nr <= r*bottom_diff)   or
                        (ng <= g*bottom_diff)   or
                        (nb <= b*bottom_diff)
                    ): continue
                    else: toExpand.append([xset, yset])

                lastAm = len(self.LocationCache)

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
