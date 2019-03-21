#// Author Jack Hales, 17-year-old Australian kas.nsw.edu.au Student
#// --
#// BitMap manipulation, BitMap refers to the process of creating a
#// black-background image that contains a prominent set of colours
#// that are significant in meaning.

#// Image.fromarray(numpyarray[.astype('uint8')], 'RGB')

import time, random
import numpy as np
from PIL import Image, ImageDraw

BitMap = Image.open("alphabet-bitmap-ds/face.jpg")
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


class PixelArray(object):
    # - dynamically set variables
    # Squares
    # OGPixelArray is a numpy array

    def __init__(self, PA):
        self.OGPixelArray = PA
        self.Squares = []
        self.SquareCache = []

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
        insertX, insertY, iteration = 0, 0, 0
        for i in range(0, (xSplit * ySplit)):
            iteration = i+1
            # - storing into the "bundled" array to return
            # later
            bundled[insertY, insertX] = PixelArr[storeY, storeX]
            self.SquareCache[storeY][storeX] = [i, insertY, insertX]
            print(storeY, storeX)
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




PA = PixelArray(PixelArr)
PA  .ExpoFilter()
PA  .SortSquares()
print(PA.Squares[3][3, 2])


#// Quick anti-alias removal, black & white ONLY


# print(pixel_array)

#preview the edited image
# im2 = Image.fromarray(pixel_array.astype("uint8"), "RGB")

# def square_bundler(x_start, y_start):

# Iterating in the right order to get the top-left x/y value
# set out appropriately.
# def sort_all_squares():




def is_empty(square):
    # print (square)
    # print (len(square))
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
# SAYING
# def reverse_squares(sqrs):
#
#
# # returns the xy
# def reverse_specific_square_for_xy(sqr, sqr_nbr)

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
#
# # specifies the runline for the squares, to
# # get all of the points in the correct direction
# def runline(sqrs):
#     pass



















# sqrs = sort_all_squares()
# for i in range(1, total_squares+1):
#     print(str(is_empty(sqrs[i-1]))+" ", end="")
#     if i%(by)==0:
#         print()

# bit_map.show()
# sqrs[0][0, 0] = [255, 255, 255]
# pa = squares2pa(sqrs)
