from PIL import Image, ImageDraw
import random, time, math, textwrap, sys, os
import numpy as np
















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
    def Complementary(self, reset=True):
        # - colour imparting
        if self.colour2 != None and reset: self.colour1, self.colour2 = None, None
        if self.colour1 == None: self.colour1 = self.Random()
        else: self.colour2 = Complementary(self.colour1)
        # conditionally returning colour1 or 2
        return self.colour1 if self.colour2 == None else self.colour2
















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
            # print(nodeStorage)
            for b in range(0, nodeAmount):
                if b != i and random.randint(0,10) > 9: #Parent does not equal the second check, connect B to I
                    firstNode = nodeStorage[i]
                    secndNode = nodeStorage[b]
                    draw.line([(firstNode[0], firstNode[1]), (secndNode[0], secndNode[1])], RandomColour(), random.randint(4,7))

    """
    To use the given weights variable to define the randomness of each
    positional movement (up/down/left/right) starting from the given xy,
    with the boundings telling the loop where to stop in terms of the
    drawing needle's placement.
    """
    lastxy = False

    def TrackingLine(self, weights, xy=False, boundby="a", colour='purple', getfromlast=False):
        global draw, size

        if xy == False: x, y = random.randint(0, size[0]), 1
        else: x, y = xy[0], xy[1]

        # print(getfromlast)
        if getfromlast == True:
            if self.lastxy == False:
                pass
            else:
                x, y = self.lastxy[0], self.lastxy[1]

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
        CLR = Colour()
        c   = CLR.Complementary() if colour == "random" else colour
        while (x <= bounds["right"]) and (y >= bounds["up"]) and (y <= bounds["down"]) and (x >= bounds["left"]):

            movement = random.uniform(0, total_weight)
            if movement < weights[0]: #UP
                y = y - 1
            elif movement < weights[0]+weights[1]: #DOWN
                y = y + 1
            elif movement < weights[0]+weights[1]+weights[2]: #LEFT
                x = x - 1
            else: #RIGHT
                x = x + 1

            self.ColourPixelAt(x=x, y=y, width=1, colour=c)
            iterations += 1
            if iterations % 500000 == 0: Progress()

        self.lastxy = [x, y]
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




















"""Managing the overall application"""
class BitmapManager:

    Template = None

    """
    Outputting into the ./development_progress folder in order for a working product
    """
    def Progress(self, optionalOutput=False):
        global current_progress
        filename = "development_progress/PROGRESS_{0}.jpg".format(current_progress)
        im.save(filename)
        print("-- sp -- :: {0}".format(optional_output))
        current_progress = current_progress + 1

    """
    Placing a Managed image into self.Template
    """
    def Template(self, location):
        self.Template = Image.open(location)

    """
    Setting up the location for outputting into, with append
    """
    def Output(self, location):
        self.OutputName = location

    # def PA =

    """
    Take the self.Template, and run the process to return the Series variable
    PixelArray (dependency injection, bitmap.PixelArray class).
    """
    def ExtractSeries(self, PA):
        # Creating a new PixelArray for the self.Template
        Pix = PA(np.array(self.Template))
        Pix.AARemove()
        Pix.SaveOG()
        Pix.SortSquares()
        # Pix.PrintSquareMap()
        Pix.Path()
        Series = Pix.PathFormat()
        self.PA = Pix
        return Series

    """
    Setting up an internal variable for our new image.
    This is going to be our primary output.
    """
    def Prep(self, color=(255, 255, 255)):
        self.OutputImage  = Image.new("RGB", (self.Template.size[0], self.Template.size[1]), color=color)
        self.TemplateSize = [self.Template.size[0], self.Template.size[1]]
        return self

    """
    Taking a PixelArray series and applying it to the self.OutputImage
    blank canvas
    """
    def ApplySeries(self, Series):
        global size, draw
        Background, Body = BG(), Bodies()
        size, draw = self.TemplateSize, ImageDraw.Draw(
            # The object which is manipulated by ApplySeries
            self.OutputImage
        )

        z = 0
        for DrawData in Series:
            # Extracting from drawing format.
            X, Y, Angle, Direction, SN, Dir = DrawData
            Bounds = {
                "up":    Direction[0],
                "down":  Direction[1],
                "left":  Direction[2],
                "right": Direction[3]}
            Body.Brush(xy=[X, Y], angle=Angle,
                power="high",
                boundby=Bounds,
                colour="random",
                # getfromlast=(False if z == 0 else True))
                getfromlast=False)
            # save
            # self.Save("renderprocess={0}".format(z))
            # if z == 5: break
            print("painting dir {0}/{3} from {1},{2}".format(Angle, X, Y, Direction))
            print()
            z += 1
        print("total of {0}".format(z))
        return self

    """
    Taking the self.OutputImage and applying a naming
    prefix to place it in the required place.
    """
    def Save(self, append):
        self.CacheAppend = append
        self.OutputImage.save("{0}-{1}.png".format(self.OutputName, append))
        return self

    def SaveTemplate(self):
        self.Template.save("{0}-OGTemplate-{1}.png".format(self.OutputName, self.CacheAppend))
        return self
