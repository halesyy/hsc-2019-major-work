from PIL import Image, ImageDraw
import random, time

def RandomColour():
    c = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    colour = "#"
    for i in range(0,6):
        colour = colour + random.choice(c)
    return colour


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
            siz = random.randint(1,3)
            c   = random.choice(["a", "b", "c", "d", "e", "f"])
            draw.rectangle([(rx1, ry1), (rx1+siz, ry1+siz)], RandomColour())

class Bodies:
    def RandomPaddedCoords(self, pixel_padding):
        global size
        #x
        x = random.randint(0+pixel_padding, size[0]-pixel_padding)
        y = random.randint(0+pixel_padding, size[1]-pixel_padding)
        return [x, y]

    def GenerateNodes(self, colour):
        nodeAmount = 4
        nodeStorage = []

        #/ Generate the nodes coords on the screen.
        for i in range(0, nodeAmount):
            nodeStorage.append(self.RandomPaddedCoords(0))

        #/ Draw: .line(xy, fill=None, width=0, joint=None), iterating each generated node and writing lines
        #/ to the lines which are NOT part of the array previously.
        for i in range(0, nodeAmount):
            print(nodeStorage)
            for b in range(0, nodeAmount):
                if b != i and random.randint(0,10) > 5: #Parent does not equal the second check, connect B to I
                    firstNode = nodeStorage[i]
                    secndNode = nodeStorage[b]
                    draw.line([(firstNode[0], firstNode[1]), (secndNode[0], secndNode[1])], colour, random.randint(4,7))

#// Image setup
size = [10000, 10000]
im = Image.open("op.jpg")
draw = ImageDraw.Draw(im)

#// Background
BG = BG()
BG.stars(10000)

#// Bodies
Bodies = Bodies()
Bodies.GenerateNodes("#c21f1f")
Bodies.GenerateNodes("#c21f1f")
Bodies.GenerateNodes("#c21f1f")

im.save("op-af.jpg")
