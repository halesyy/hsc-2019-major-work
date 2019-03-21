#// Author Jack Hales, 17-year-old Australian kas.nsw.edu.au Student
#// --
#// BitMap manipulation, BitMap refers to the process of creating a
#// black-background image that contains a prominent set of colours
#// that are significant in meaning.

#// Image.fromarray(numpyarray[.astype('uint8')], 'RGB')

import time, random
import numpy as np
from PIL import Image, ImageDraw

BitMap = Image.open("alphabet-bitmap-ds/a.jpg")
PixelArr = np.array(BitMap)

xs = BitMap.size[0]
ys = BitMap.size[1]

#// Manual Colour-coding array
#// To be in JSON file one day

#// Requirement splitting for Vision rules
#// % value, 0.25 = 25% means splitting into 4 parts x 4 parts

by = 4
split = 1 / by
squares = int(1 / split)
squaresx = squares
totalSquares = int(squares*squares)
squarePixels = (xs*ys)/squares

xSplit = int((xs) / (1 / split))
ySplit = int((ys) / (1 / split))


# | Quick anti-alias removal, black & white ONLY,
# | lesser is reduced to black, and higher is
# | ceiling'd to white
# for i in range(0, xs):
#     for b in range(0, ys):
#         if pixel_array[i, b][0] < 200:
#             pixel_array[i, b] = [0, 0, 0]
#         else:
#             pixel_array[i, b] = [255, 255, 255]

# | Quick anti-alias removal, black & white ONLY,
# | lesser is reduced to black, and higher is
# | ceiling'd to white
# for i in range(0, xs):
#     for b in range(0, ys):
#         if pixel_array[i, b][0] < 200:
#             pixel_array[i, b] = [0, 0, 0]
#         else:
#             pixel_array[i, b] = [255, 255, 255]


class PixelArray(object):
    # - dynamically set variables
    # Squares
    # OGPixelArray is a numpy array

    def __init__(self, PA):
        self.OGPixelArray = PA
        self.Squares = []
        # - convert the "pixel array" location
        # into the square information and insert
        # seq
        self.PixelArrCache = np.zeros(shape=(xSplit*xSplit, ySplit*ySplit), dtype=list)

    # -
    def ExpoFilter(self):
        PixelArr = self.OGPixelArray
        for i in range(0, xs):
            for b in range(0, ys):
                if PixelArr[i, b][0] < 200:
                    PixelArr[i, b] = [0, 0, 0]
                else:
                    PixelArr[i, b] = [255, 255, 255]
        self.OGPixelArray = PixelArr

    def SortSquares(self):
        PixelArr = self.OGPixelArray
        Squares = [None for f in range(0, squares*squares)]
        startX, startY, iteration = 0, 0, 0
        for i in range(0, int(squares*squares)):
            # print(startX, startY)
            iteration += 1
            Squares[i] = self.SquareBundlerStartFrom(i, startX, startY)
            if iteration % int(xs/xSplit) == 0:
                startY = startY + ySplit
                startX = 0
            else:
                startX = startX + xSplit
        self.Squares = Squares

    def SquareBundlerStartFrom(self, squareNo, xStart, yStart):
        # Presetting the values for the bundled variables in a
        # 2D Numpy Array
        bundled = np.zeros(shape=(xSplit, ySplit), dtype=object)
        # Where we will start from for finding the X/Y values
        PixelArr = self.OGPixelArray
        storeX, storeY = xStart, yStart
        # For Inserting
        # print(squareNo)
        insertX, insertY, iteration = 0, 0, 0
        for i in range(0, (xSplit * ySplit)):
            iteration = i+1
            # - storing into the "bundled" array to return
            # later
            # - storing in the bundle return [Y, X]
            bundled[insertY, insertX] = PixelArr[storeY, storeX]
            # - storing in the caches [Y, X]
            self.PixelArrCache[storeY, storeX] = {"square": squareNo, "insertY": storeY, "insertX": storeX, "squareLocX": insertY, "squareLocY": insertX}
            if (iteration % int(xSplit) == 0):
                storeX = xStart
                storeY +=  1
                insertX = 0
                insertY += 1
            else:
                storeX += 1
                insertX += 1
        # bundled[0, 0] = [255, 255, 255]
        return bundled

    def SquareToPixelArr(self, SquareNo, Coords):
        # print(self.OGPixelArray)
        # - coords = [X, Y]
        for eachInfoBundle in self.PixelArrCache:
            for cacheInformation in eachInfoBundle:
                # print(cacheInformation)
                if (SquareNo == cacheInformation["square"]) and (Coords[0] == cacheInformation["squareLocX"]) and (Coords[1] == cacheInformation["squareLocY"]):
                    return cacheInformation

    def Square2PAEditor(self, SquareNo, Coords):
        # print(SquareNo, Coords, "\n")
        CInformation = self.SquareToPixelArr(SquareNo, Coords)
        return [CInformation["insertY"], CInformation["insertX"]]


    def Change(self, src="PixelArr", xy=[], squareno=False, to=[]):
        # - src = PixelArr or Squares,
        # - Each edit has to edit the OGPixelArray
        x, y = xy[0], xy[1]
        # - Default format: [Y, X] when accessing
        if src == "Squares":
            SquareNo = squareno
            EditInfo = self.Square2PAEditor(SquareNo, [x, y])
            self.OGPixelArray[EditInfo[1], EditInfo[0]] = to

    def ShowOG(self):
        OGPA = self.OGPixelArray
        im = Image.fromarray(OGPA)
        im.show()
        return self

    def SaveOG(self):
        OGPA = self.OGPixelArray
        im = Image.fromarray(OGPA)
        im.save("og.png")
        return self



PA = PixelArray(PixelArr)
PA  .ExpoFilter()
PA  .SortSquares()

# PA.ShowOG().SaveOG()

PA.Change("Squares", xy=[1, 1], squareno=15
, to=[255, 255, 255])
# PA.Change("Squares", xy=[1, 2], squareno=15, to=[255, 255, 255])
# PA.SaveOG()
PA.ShowOG()


# EditInfo = PA.Square2PAEditor(6, [0, 0])
# print(EditInfo)














# | Quick square is-empty clause, checking
# | if data in the square is totally black,
# | if so, return 1, else return 0.
def is_empty(square):
    is_empty_re = 1
    for a in range(len(square)):
        for b in range(len(square[a])):
            if square[a][b][0] == 255:
                is_empty_re = 0
    return is_empty_re



# converting from the squrs-format sort_all_squares output,
# into the opposite, so we can transform and go backwards
# as a backwards integration
# basically, use-test is to be able to make a tiny change
# to sqrs, such as implementation of a small pixel,
# then be able to go backwards...
# that is a FUCKING DIFFICULT THING TO ACHIEVE, I AM JUST
def squares2pa(sqrs):
    global squaresx, total_squares
    # pa = np.zeros((xs, ys))
    # pa = [[0 for p in range(total_squares)] for q in range(total_squares)]
    pa = [[0 for p in range(total_squares)] for q in range(total_squares)]
    print(pa)
    # print(pa[0])
    # print(squares)
    # each new array is a new array
    for sqr, it in zip(sqrs, range(1, total_squares+1)):

        ycomp = 0 # increase this by 4 each time we
                 # do a 4-square iteration

        for xv in range(xs):
            for yv in range(ys):
                pa[yv+ycomp][xv] = sqr[xv, yv]
                # print(yv+comp)
                # print(xv, yv+comp)

        if it%squaresx: ycomp += squaresx

        # print(row)
    print(pa)
        # pass







def gradient_check(xy1, xy2):
    # getting the slope from xy1 to xy2, essentially to get the positioning
    # and get a valuemeter for it
    # if xy2 is to the LEFT of  xy1, then they are going left
    # if xy2 is to the UNDER of xy1, then they are going down
    # see the pattern? xy1 is the initial, and xy2 helps give
    # reference.
    pass





# class PixelArray(object):
#
#     # | -------------------------------------------
#     # | Giving the pixel array
#     def __init__(self, PA):
#         self.OGPA = PA
#
#     # | -------------------------------------------
#     # | Taking self.OGPA and sorting into squares
#     def SquareSort(self):
#
#         allSquares = [None for f in range(0, squares*squares)]
#         startx, starty, iter = 0, 0, 0
#         for i in range(int(squares*squares)):
#
#             iter = iter + 1
#
#             allSquares[i] = self.SquareBundler(startx, starty, squareno=i)
#
#             if iteration % int(xs/x_split) == 0:
#                 starty, startx = (starty + ysplit), 0
#             else:
#                 startx += x_split
#         return allSquares
#
#     # | -------------------------------------------
#     # | Takes a square and bundles into array, but
#     # | is tasked with storing cache data for each
#     # | squareno/x/y value with it's original
#     # | pairing when reaching into the OG Array.
#     # | (self.OGPA) <-
#     def SquareBundler(startx, starty, squareno):
#         global x_split, y_split, split, squares, square_pixels, pixel_array
#         # Presetting the values for the bundled variables in a
#         # 2D Numpy Array
#         bundled = np.zeros(shape=(x_split, y_split), dtype=object)
#         # Where we will start from for finding the X/Y values
#         store_x = x_start
#         store_y = y_start
#         # For Inserting
#         insert_x = 0
#         insert_y = 0
#         for i in range(0, (x_split * y_split)):
#             iteration = i+1
#             # Seems that the y/x values are swapped, so we have
#             # to later chance that if we are to set back as image.
#             # @NOTE this.
#             bundled[insert_y, insert_x] = pixel_array[store_y, store_x]
#
#             if (iteration % int(x_split) == 0):
#                 store_x = x_start
#                 store_y = store_y + 1
#                 insert_x = 0
#                 insert_y = insert_y + 1
#             else:
#                 store_x  = store_x + 1
#                 insert_x = insert_x + 1
#         # bundled[0, 0] = [255, 255, 255]
#         return bundled



# PIXAR = PixelArray(pixel_array)
# print(PIXAR.OGPA)
# PixelArray.SquareSort()












# sqrs = sort_all_squares()
# for i in range(1, total_squares+1):
#     # print(str(is_empty(sqrs[i-1]))+" ", end="")
#     if i%(by)==0:
#         # print()
#         pass

# sqrs[0][0, 0] = [255, 255, 255]
# pa = squares2pa(sqrs)

# should return a pixel_array format
# pa = Image.fromarray(pa)
# pa.show()

# sqrs[1][0, 2] = [255, 255, 255]
# sqrs[0][0, 3] = [255, 255, 255]
# sqrs[0][0, 4] = [255, 255, 255]

# print(pixel_array)
# print(pixel_array[0, 0])

# arr = np.array(bm)
# print(arr[32, 32])
# pixel_array[0, 0] = [255, 255, 255]

# bit_map.show()
# sqrs[0][0, 0] = [255, 255, 255]
# pa = squares2pa(sqrs)
