from PIL import Image, ImageDraw
import random, time, math, textwrap, sys, os

class Colour:

    colour1 = None
    colour2 = None

    """Returning a random hex colour value"""
    def Random(self):
        c = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        # c = ["0", "1", "2", "3", "4", "5"] #darker
        # c = ["a", "b", "c", "d", "e", "f"] #brighter
        # c = random.choice(c)
        # colour = "#{0}{1}{2}{3}{4}{5}".format(c,c,c,c,c,c)
        colour = "#"
        for i in range(0,6): colour += random.choice(c)
        return colour

    """Returns the complimentary colour of the given HEX colour"""
    def GetComplimentary(self, hex):
        # - #abcdef
        hex  = hex.replace('#', '')
        hexp = textwrap.wrap(hex, 2)
        for i, h in enumerate(hexp):
            hexp[i] = 255-int("0x{0}".format(h), 0)
        # print(hexp)
        for i, h in enumerate(hexp):
            # print(i, h)
            # print(int(h))
            # print(hexp)
            # print(hex(int(h)))
            hexp[i] = h.to_bytes(1, byteorder='big').hex()
        return "{0}{1}".format("#", "".join(hexp))

    """Manager for comp colours, in terms of getting first, second, and flushing variables"""
    def Complementary(reset=True):
        # - colour imparting
        if self.colour2 != None and reset: self.colour1, self.colour2 = None, None
        if self.colour1 == None: self.colour1 = RandomColour()
        else: self.colour2 = Complementary(self.colour1)
        # conditionally returning colour1 or 2
        return self.colour1 if self.colour2 == None else return self.colour2

class Manager:

    """Outputting into the ./development_progress folder in order for a working product"""
    def Progress(self, optionalOutput=False):
        global current_progress
        filename = "development_progress/PROGRESS_{0}.jpg".format(current_progress)
        im.save(filename)
        print("-- sp -- :: {0}".format(optional_output))
        current_progress = current_progress + 1


"""
The "background" functions controlling the look of
the furtherst-back layer of image handling.
"""
class BG:
    def stars(self, density):
        for i in range(0, density):
            rx1 = random.randint(0, size[0])
            ry1 = random.randint(0, size[1])
            siz = random.randint(0,5)
            # c   = random.choice(["0", "1", "2", "3", "4", "5"])
            # colour = "#{0}{1}{2}{3}{4}{5}".format(c,c,c,c,c,c)
            colour = RandomColour()
            # colour = RandomColour()
            draw.rectangle([(rx1, ry1), (rx1+siz, ry1+siz)], colour)

"""
The body managers, as in all of the managers for the
content of the interesting image, including brushes, etc..
"""
class Bodies:
    def RandomPaddedCoords(self, pixel_padding):
        global size
        #x
        x = random.randint(0+pixel_padding, size[0]-pixel_padding)
        y = random.randint(0+pixel_padding, size[1]-pixel_padding)
        return [x, y]

    def ColourPixelAt(self, x, y, width, colour):
        draw.rectangle([(x, y), (x+width,y +width)], colour)

    def GenerateNodes(self, colour):
        nodeAmount = 18
        nodeStorage = []

        #/ Generate the nodes coords on the screen.
        for i in range(0, nodeAmount):
            nodeStorage.append(self.RandomPaddedCoords(0))

        #/ Draw: .line(xy, fill=None, width=0, joint=None), iterating each generated node and writing lines
        #/ to the lines which are NOT part of the array previously.
        for i in range(0, nodeAmount):
            print(nodeStorage)
            for b in range(0, nodeAmount):
                if b != i and random.randint(0,10) > 9: #Parent does not equal the second check, connect B to I
                    firstNode = nodeStorage[i]
                    secndNode = nodeStorage[b]
                    draw.line([(firstNode[0], firstNode[1]), (secndNode[0], secndNode[1])], RandomColour(), random.randint(4,7))

    #// Purpose of funtion is to track itself randomly and create a completely random
    #// set of lines.
    #// down_weight is a value which is then divided by 10000 to get the addition
    #// to creating the excess that the down movement is given leverage to, meaning
    #// 100 means it is 1.01 (1+100/10000) quicker.
    """
    To use the given weights variable to define the randomness of each
    positional movement (up/down/left/right) starting from the given xy,
    with the boundings telling the loop where to stop in terms of the
    drawing needle's placement.
    """
    def TrackingLine(self, weights, xy=False, boundby="a", colour='purple', getfromlast=False):
        global lastxy

        if xy == False: x, y = random.randint(0, size[0]), 1
        else: x, y = xy[0], xy[1]

        # print(getfromlast)
        if getfromlast == True:
            x, y = lastxy[0], lastxy[1]
            # print("Getting from last")

        # print("tl: {0}, {1}".format(x, y))
        iterations = 0
        total_weight = sum(weights)
        # predefinedColour = colour

        bounds = {
            "down":  size[1],   # within bottom
            "up":    0,           # within top
            "right": size[0],  # within right
            "left":  0          # within left
        }

        if boundby == "a": pass #all
        else:
            for boundDefiner in boundby:
                if boundDefiner == 'left' or boundDefiner == 'up':
                    bounds[boundDefiner] += boundby[boundDefiner]
                elif boundDefiner == 'down' or boundDefiner == 'right':
                    bounds[boundDefiner] -= boundby[boundDefiner]

        # RULES:
        c = ComRandom() if colour == "random" else colour
        while (x < bounds["right"]) and (y > bounds["up"]) and (y < bounds["down"]) and (x > bounds["left"]):
            # c = ComRandom() if colour == "random" else colour

            movement = random.uniform(0, total_weight)
            if movement < weights[0]: #UP
                # y = y - 1 if y + 1 > 0 else y + 1
                y = y - 1
            elif movement < weights[0]+weights[1]: #DOWN
                y = y + 1
            elif movement < weights[0]+weights[1]+weights[2]: #LEFT
                # x = x - 1 if x - 1 > 0 else x + 1
                x = x - 1
            else: #RIGHT
                # x = x + 1 if x + 1 < size[0] else x - 1
                x = x + 1

            # print("at {0},{1} drawing".format(x, y))
            self.ColourPixelAt(x=x, y=y, width=1, colour=c)
            iterations = iterations + 1
            if iterations % 500000 == 0:
                Progress()

        lastxy = [x, y]
        # print("Completion took {0} iterations...".format(iterations))

    """
    Setting up a "presentation", providing the times in which to change
    different aspects, when to save, stop, all dictated by the iteration #.
    Once it hits one of the iteration #'s, will change intermal self.TrackingLine
    function call weights to change the engine's dynamics.
    """
    def SAS_TrackingLine(self, presentation, xy=False):
        if xy == False:
            x = random.randint(0, size[0])
            y = 0
        else:
            x = xy[0]
            y = xy[1]
        #
        iter = 0
        movements = [0,0,0,0]
        current_weightset = []
        predefinedColour = ""
        break_loop = False
        while y != size[1]:
            for i in range(0, len(presentation)):
                if iter == presentation[i]["time"]:
                    old_weightset = current_weightset
                    old_colour = predefinedColour
                    predefinedColour = RandomColour()
                    current_weightset = presentation[i]["weights"]
                    #saving into saves variable
                    if current_weightset == "save_xy":
                        saves[presentation[i]["save_as"]] = [x,y]
                        print("Saved xy to {0}".format(presentation[i]["save_as"]))
                        current_weightset = old_weightset
                        predefinedColour  = old_colour
                    #end the loop execution
                    if current_weightset == "stop":
                        print("Hit a stop, finished!")
                        break_loop = True

            if break_loop:
                break

            movement = random.uniform(0, sum(current_weightset))
            # print(movement)
            if movement < current_weightset[0]: #UP
                y = y - 1 if y + 1 > 0 else y
                # y = y - 1
                movements[0]+=1
            elif movement < current_weightset[0]+current_weightset[1]: #DOWN
                y = y + 1
                movements[1]+=1
            elif movement < current_weightset[0]+current_weightset[1]+current_weightset[2]: #LEFT
                x = x - 1 if x - 1 > 0 else x + 1
                # x = x - 1
                movements[2]+=1
            else: #RIGHT
                x = x + 1 if x + 1 < size[0] else x - 1
                # x = x + 1
                movements[3]+=1

            self.ColourPixelAt(x, y, 1, predefinedColour)
            iter = iter + 1
            if iter % 500000 == 0:
                Progress(movements)

        print("Completion took {0} iterations...".format(iter))

    """
    Bodies.Brush()
    A directional brush stroke, applying a "random" grade algorithm.
    """
    def Brush(self, xy, angle, power="soft", boundby="a", colour='random', getfromlast=False):
        powersets = {
            "low": 0.7, "medium": 4, "high": 1*10000, "superhigh": 10000*10000
        }

        while angle >= 360: angle -= 360
        base, amplify = 1, powersets[power]
        up, right, down, left = base, base, base, base
        setup = [up, right, down, left]

        selector = math.floor(angle / 90)
        selectorAssistant = 0 if selector == 3 else selector+1

        # bringing underAngle to an under90 value
        underAngle = angle
        while underAngle >= 90: underAngle -= 90

        SecondaryAngler = round((underAngle / 90), 2) # minor
        PrimaryAngler   = 1 - SecondaryAngler # major

        setup[selector]          = round(base*(PrimaryAngler*amplify)+base, 2)
        setup[selectorAssistant] = round(base*(SecondaryAngler*amplify)+base, 2)

        # - re-packing setup for general form
        setup = [setup[0], setup[2], setup[3], setup[1]]
        self.TrackingLine(setup, xy, boundby=boundby, colour=colour, getfromlast=getfromlast)

    """
    Bodies.Tspurt()
    Applies a "spread" algorithm on the xy coordinate.
    """
    def Tspurt(self, xy, colour="random", padding=10, power="medium"):
        ur, s = True, 5
        c = RandomColour() if colour == "random" else colour
        for deg in range(0, 360, 9):
            print(c)
            self.brush(xy=xy, angle=deg, power=power, boundby=[
                ["left",  xy[0]-padding+(random.randint(1, 5*s)*ur)],
                ["right", xy[1]+padding+(random.randint(1, 5*s)*ur)],
                ["down",  xy[0]+padding+(random.randint(1, 5*s)*ur)],
                ["up",    xy[1]-padding+(random.randint(1, 5*s)*ur)]
            ], colour=c)

"""Setting up classes for runtime"""
BG, Bodies = BG(), Bodies()

rs   = Image.new("RGB", (im.size[0], im.size[1]), color=(255, 255, 255))
imBB = Image.new("RGB", (im.size[0], im.size[1]), color=(255, 255, 255))
# I've forgotten what these do

xs, ys = im.size[0], im.size[1]
size = [xs, ys]

draw = ImageDraw.Draw(im)
lastxy, GetFromLast = [], False

"""Implementing previous classes"""
sys.path.append(os.path.abspath("../BITMAP"))
from Bitmap import *

BitmapTemplate = Image.open("../BITMAP/alphabet-bitmap-ds/b.jpg")
PA = PixelArray(np.array(BitmapTemplate))
PA.AARemove()
PA.SaveOG()
PA.SortSquares()
PA.PrintSquareMap()
PA.Path()
Series = PA.PathFormat()

#   O < < (YEET ON THIS CODE)
# \_|_/   (-----------------)
#   |     (-----------------)
#  / \    (-----------------)
# /  |    (-----------------)

z, draw = 0, ImageDraw.Draw(imBB)

# pp(Series)

for S in Series:
    X, Y, Angle, Direction, SN, Dir = S
    Bounds = {
        "up":    Direction[0],
        "down":  Direction[1],
        "left":  Direction[2],
        "right": Direction[3]}
    Bodies.brush([X, Y], angle=Angle,
        power="high",
        boundby=Bounds,
        colour="random",
        getfromlast=(False if z == 0 else True))
    z += 1

PA.Trim(64, [21, 210, 123])
PA.SaveOG()

im.save("op-af.png")
imBB.save("op-bb.png")
# im.save("op-af.jpeg")
# im.save("op-af.jpg")
