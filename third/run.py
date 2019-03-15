from PIL import Image, ImageDraw
import random, time, math

def RandomColour():
    c = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    # c = ["0", "1", "2", "3", "4", "5"] #darker
    # c = ["a", "b", "c", "d", "e", "f"] #brighter
    # c = random.choice(c)
    # colour = "#{0}{1}{2}{3}{4}{5}".format(c,c,c,c,c,c)
    colour = "#"
    for i in range(0,6): colour += random.choice(c)
    return colour


def Progress(optional_output=False):
    global current_progress
    filename = "development_progress/PROGRESS_{0}.jpg".format(current_progress)
    im.save(filename)
    print("-- sp -- :: {0}".format(optional_output))
    current_progress = current_progress + 1

#// -------------------------------------
#// Background module, in charge of all
#// functions which are involved in the
#// management of the background-manips.
#// -------------------------------------
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
    def TrackingLine(self, weights, xy=False, boundby="a", colour='purple'):
        if xy == False: x, y = random.randint(0, size[0]), 1
        else: x, y = xy[0], xy[1]

        print("tl: {0}, {1}".format(x, y))
        iterations = 0
        total_weight = sum(weights)
        predefinedColour = colour

        bounds = {
            "down":  size[1],   # within bottom
            "up":    0,           # within top
            "right": size[0],  # within right
            "left":  0          # within left
        }

        if boundby == "a": pass #all
        else:
            for boundSet in boundby:
                # each presents: ["up/down/left/right"] and a numeric val
                # numeric value corresponds to where it has to be inside of
                # for that section
                # ["left", 4] means val has to break once reaching 4
                direction = boundSet[0]
                stoppingPoint = boundSet[1]
                bounds[direction] = stoppingPoint

        print(bounds)
        while (y < bounds["down"]) and (y > bounds["up"]) and (x < bounds["right"]) and (x > bounds["left"]):
            print("Going to draw!")
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
            self.ColourPixelAt(x=x, y=y, width=1, colour=predefinedColour)
            iterations = iterations + 1
            if iterations % 500000 == 0:
                Progress()
        # print("Completion took {0} iterations...".format(iterations))

    # Setting up a presentation for the tracking line, to change at certain
    # iterations.
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

    # Brush stroke, simple
    def brush(self, xy, angle, power="soft", boundby="a", colour='random'):
        # print(xy)
        # print(boundby)
        powersets = {
            "low": 0.7,
            "medium": 4,
            "high": 1*(10000)
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

        # re-packing setup for general form
        setup = [setup[0], setup[2], setup[3], setup[1]]
        self.TrackingLine(setup, xy, boundby=boundby, colour=colour)

    def tspurt(self, xy, colour="random", padding=10, power="medium"):
        ur = False
        for deg in range(0, 360, 9):
            c = colour if colour != "random" else RandomColour()
            self.brush(xy=xy, angle=deg, power=power, boundby=[
                ["left",  xy[0]-padding],
                ["right", xy[1]+padding],
                ["down",  xy[0]+padding],
                ["up",    xy[1]-padding]
            ], colour=c)

#// Image setup
BG, Bodies, size = BG(), Bodies(), [128, 128]
im   = Image.open("../BITMAP/alphabet-bitmap-ds/big-circle.jpg")
draw = ImageDraw.Draw(im)

for i in range(1):
    current_progress = 0
    saves = {}
    # BG.stars(int((size[0]*size[1])/1000))
    # Bodies.tspurt(xy=[63, 63], power="high",   padding=5)
    Bodies.tspurt(xy=[20, 92], power="low",    padding=5)
    Bodies.ColourPixelAt(20, 92, 2, "#c21f1f")
    Bodies.tspurt(xy=[92, 18], power="medium", padding=5)

im.save("op-af.png")
im.save("op-af.jpeg")
im.save("op-af.jpg")










#J
# Bodies.SAS_TrackingLine([
#     {
#         "time": 0,
#         "weights": [1000,1050,1000,1000]
#     },
#     {
#         "time": 90000,
#         "weights": [980,980,1070,1000]
#     },
#     {
#         "time": 150000,
#         "weights": [1050,1000,1000,1000]
#     },
#     {
#         "time": 200000,
#         "weights": "stop"
#     }
# ], [1500, 400])
#
#
#
#
# #A
# Bodies.SAS_TrackingLine([
#     {
#         "time": 0,
#         "weights": [1050,1000,1000,1000]
#     },
#     {
#         "time": 50000,
#         "weights": "save_xy",
#         "save_as": "a_mid"
#     },
#     {
#         "time": 100000,
#         "weights": [980,980,1000,1050]
#     },
#     {
#         "time": 150000,
#         "weights": [1000,1050,1000,1000]
#     },
#     {
#         "time": 250000,
#         "weights": "stop"
#     }
# ], [2250, 1600])
# #A-
# Bodies.SAS_TrackingLine([
#     {
#         "time": 0,
#         "weights": [1000,1000,1000,1050]
#     },
#     {
#         "time": 70000,
#         "weights": "stop"
#     }
# ], saves["a_mid"])
#
#
#
# #C
# Bodies.SAS_TrackingLine([
#     {
#         "time": 0,
#         "weights": [1000,1000,1070,1000]
#     },
#     {
#         "time": 60000,
#         "weights": [1000,1050,1000,1000]
#     },
#     {
#         "time": 150000,
#         "weights": [1000,1000,1000,1050]
#     },
#     {
#         "time": 250000,
#         "weights": "stop"
#     }
# ], [5000, 400])
#
#
#
# #K
# Bodies.SAS_TrackingLine([
#     {
#         "time": 0,
#         "weights": [1000,1050,1000,1000]
#     },
#     {
#         "time": 50000,
#         "weights": "save_xy",
#         "save_as": "k_middle"
#     },
#     {
#         "time": 100000,
#         "weights": "stop"
#     }
# ], [6000, 400])
# #k-topright
# Bodies.SAS_TrackingLine([
#     {
#         "time": 0,
#         "weights": [1050,1000,1000,1050]
#     },
#     {
#         "time": 60000,
#         "weights": "stop"
#     }
# ], saves["k_middle"]) #got the coords of the middle point of K
# #k-bottom-right
# Bodies.SAS_TrackingLine([
#     {
#         "time": 0,
#         "weights": [1000,1050,1000,1050]
#     },
#     {
#         "time": 60000,
#         "weights": "stop"
#     }
# ], saves["k_middle"]) #got the coords of the middle point of K

# im.save("op-af.jpg")
