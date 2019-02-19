#// Author Jack Hales, 17-year-old Australian kas.nsw.edu.au Student
#// --
#// BitMap manipulation, BitMap refers to the process of creating a
#// black-background image that contains a prominent set of colours
#// that are significant in meaning.

#// Image.fromarray(numpyarray[.astype('uint8')], 'RGB')

import time, random
import numpy as np
from PIL import Image, ImageDraw

bit_map     = Image.open("alphabet-bitmap-ds/j.jpg")
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
total_squares = int(squares*squares)
square_pixels = (xs*ys)/squares

x_split = int((xs) / (1 / split))
y_split = int((ys) / (1 / split))

#// Quick anti-alias removal, black & white ONLY
for i in range(0, xs):
    for b in range(0, ys):
        if pixel_array[i, b][0] < 200:
            pixel_array[i, b] = [0, 0, 0]
        else:
            pixel_array[i, b] = [255, 255, 255]

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

# Don't really ever want to see this again ^^.

def is_empty(square):
    # print (square)
    # print (len(square))
    is_empty_re = 1
    for a in range(len(square)):
        for b in range(len(square[a])):
            if square[a][b][0] == 255:
                is_empty_re = 0
    return is_empty_re

























sqrs = sort_all_squares()
for i in range(1, total_squares+1):
    print(str(is_empty(sqrs[i-1]))+" ", end="")
    if i%(by)==0:
        print()

# print(is_empty(sqrs[3]))

# arr = np.array(bm)
# print(arr[32, 32])
# bm.show()
