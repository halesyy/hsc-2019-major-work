from PIL import Image, ImageDraw
import random, time

#/ Function to setup a padding that can't be picked at for random choices
def randomPadChoice(padding):
    global size
    #x
    x = random.randint(0+padding, size[0]-padding)
    y = random.randint(0+padding, size[1]-padding)
    return [x, y]

size = [10000, 10000]
im = Image.open("op.jpg")
draw = ImageDraw.Draw(im)

def background():
    backgroundDensity = 39000
    #/ Creating a background
    for i in range(0, backgroundDensity):
        rx1 = random.randint(0, size[0])
        ry1 = random.randint(0, size[1])
        siz = random.randint(2,5)
        c   = random.choice(["0", "1", "2", "3", "4", "5"])
        draw.rectangle([(rx1, ry1), (rx1+siz, ry1+siz)], "#{0}{1}{2}{3}{4}{5}".format(c, c, c, c, c, c))

def nodeConnect(colour):
    nodeAmount = 10
    nodeStorage = []

    #/ Generate the nodes coords on the screen.
    for i in range(0, nodeAmount):
        nodeStorage.append(randomPadChoice(0))

    #/ Draw: .line(xy, fill=None, width=0, joint=None)
    for i in range(0, nodeAmount):
        print(nodeStorage)
        for b in range(0, nodeAmount):
            if b != i and random.randint(0,10) > 0.9: #Parent does not equal the second check, connect B to I
                firstNode = nodeStorage[i]
                secndNode = nodeStorage[b]
                draw.line([(firstNode[0], firstNode[1]), (secndNode[0], secndNode[1])], colour, random.randint(4,12))

background()
# nodeConnect()
nodeConnect("#3de1ff")
nodeConnect("#ff2b2e")


im.save("op-af.jpg")
