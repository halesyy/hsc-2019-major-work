#// Author Jack Hales, 17-year-old Australian kas.nsw.edu.au Student
#// --
#// BitMap manipulation, BitMap refers to the process of creating a
#// black-background image that contains a prominent set of colours
#// that are significant in meaning.

#// Image.fromarray(numpyarray[.astype('uint8')], 'RGB')

import time, random
import numpy as np
from PIL import Image, ImageDraw

bit_map     = Image.open("alphabet-bitmap-ds/face.jpg")
pixel_array = np.array(bit_map)


xs = bit_map.size[0]
ys = bit_map.size[1]

#// Manual Colour-coding array
#// To be in JSON file one day


#// Requirement splitting for Vision rules
#// % value, 0.25 = 25% means splitting into 4 parts x 4 parts
by = 4
split = 1 / by
squares = int(1 / split)
squaresx = squares
total_squares = int(squares*squares)
square_pixels = (xs*ys)/squares

x_split = int((xs) / (1 / split))
y_split = int((ys) / (1 / split))


class PixelArray(object):
    def __init__(self, PA):
        self.OGPixelArray = PA



# PA = PixelArray(pixel_array)



#// Quick anti-alias removal, black & white ONLY
for i in range(0, xs):
    for b in range(0, ys):
        if pixel_array[i, b][0] < 200:
            pixel_array[i, b] = [0, 0, 0]
        else:
            pixel_array[i, b] = [255, 255, 255]

# print(pixel_array)

#preview the edited image
# im2 = Image.fromarray(pixel_array.astype("uint8"), "RGB")

def square_bundler(x_start, y_start):
    global x_split, y_split, split, squares, square_pixels, pixel_array
    # Presetting the values for the bundled variables in a
    # 2D Numpy Array
    bundled = np.zeros(shape=(x_split, y_split), dtype=object)
    # Where we will start from for finding the X/Y values
    store_x = x_start
    store_y = y_start
    # For Inserting
    insert_x = 0
    insert_y = 0
    for i in range(0, (x_split * y_split)):
        iteration = i+1
        # Seems that the y/x values are swapped, so we have
        # to later chance that if we are to set back as image.
        # @NOTE this.
        bundled[insert_y, insert_x] = pixel_array[store_y, store_x]

        if (iteration % int(x_split) == 0):
            store_x = x_start
            store_y = store_y + 1
            insert_x = 0
            insert_y = insert_y + 1
        else:
            store_x  = store_x + 1
            insert_x = insert_x + 1
    # bundled[0, 0] = [255, 255, 255]
    return bundled

# Iterating in the right order to get the top-left x/y value
# set out appropriately.
def sort_all_squares():
    all_squares = [None for f in range(0, squares*squares)]
    start_x = 0
    start_y = 0
    iteration = 0

    for i in range(0, int(squares*squares)):
        # print(start_x, start_y)
        iteration = iteration + 1
        # print("it {0} out of {1}".format(iteration, squares*squares+1))
        # print(start_x, start_y, ":")
        all_squares[i] = square_bundler(start_x, start_y)
        if iteration % int(xs/x_split) == 0:
            start_y = start_y + y_split
            start_x = 0
        else:
            start_x = start_x + x_split

    return all_squares



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



















sqrs = sort_all_squares()
for i in range(1, total_squares+1):
    # print(str(is_empty(sqrs[i-1]))+" ", end="")
    if i%(by)==0:
        # print()
        pass
# bit_map.show()
sqrs[0][0, 0] = [255, 255, 255]
pa = squares2pa(sqrs)
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

# pa = Image.fromarray(pixel_array)
# pa.show()
# pa.save('fkn-around.png')
