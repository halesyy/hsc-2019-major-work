from PIL import Image, ImageDraw
import random, time

def RandomColour():
    c = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    # c = ["0", "1", "2", "3", "4", "5"] #darker
    # c = ["a", "b", "c", "d", "e", "f"] #brighter
    # c = random.choice(c)
    # colour = "#{0}{1}{2}{3}{4}{5}".format(c,c,c,c,c,c)
    colour = "#"
    for i in range(0,6):
        colour = colour + random.choice(c)
    return colour


def Progress():
    global current_progress
    filename = "development_progress/PROGRESS_{0}.jpg".format(current_progress)
    im.save(filename)
    print("SAVED PROGRESS {0}".format(current_progress))
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
            c   = random.choice(["0", "1", "2", "3", "4", "5"])
            colour = "#{0}{1}{2}{3}{4}{5}".format(c,c,c,c,c,c)
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
    def TrackingLine(self):
        x = random.randint(0, size[0])
        y = 0
        self.ColourPixelAt(x, y, 1, RandomColour())
        iterations = 0
        while y != size[1]:
            movement = random.randint(1, 4)
            #safety net
            if movement == 1: #LEFT
                x = x - 1 if x - 1 > 0 else x + 1
                # x = x - 1
            elif movement == 2: #RIGHT
                x = x + 1 if x + 1 < size[0] else x - 1
                # x = x + 1
            elif movement == 3: #UP
                y = y - 1 if y + 1 > 0 else y + 1
                # y = y + 1
            else: #DOWN
                y = y + 1
            # if iterations > 1500000:
            #     break
            self.ColourPixelAt(x, y, 1, RandomColour())
            iterations = iterations + 1
            if iterations % 500000 == 0:
                Progress()
        print("Completion took {0} iterations...".format(iterations))


#// Image setup
size = [7680, 2160]
im = Image.open("op.jpg")
draw = ImageDraw.Draw(im)
current_progress = 0

#// Background
BG = BG()
BG.stars(7500)

#// Bodies
Bodies = Bodies()
# Bodies.GenerateNodes("#c21f1f")
# Bodies.GenerateNodes("#c21f1f")
# Bodies.GenerateNodes("#c21f1f")
for i in range(0, 1):
    Bodies.TrackingLine()


im.save("op-af.jpg")
