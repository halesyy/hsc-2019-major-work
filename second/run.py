from PIL import Image, ImageDraw
import random, time

size = [1920, 1080]
im = Image.open("op.jpg")
draw = ImageDraw.Draw(im)

nodeAmount = 12
nodeStorage = []

#/ First, generate the nodes coords.
for i in range(0, nodeAmount):
    nodeStorage.append([random.randint(0, size[0]), random.randint(0, size[1])])

#/ Draw: .line(xy, fill=None, width=0, joint=None)
for i in range(0, nodeAmount):
    print(nodeStorage)
    for b in range(0, nodeAmount):
        if b != i: #Parent does not equal the second check, connect B to I
            firstNode = nodeStorage[i]
            secndNode = nodeStorage[b]
            draw.line([(firstNode[0], firstNode[1]), (secndNode[0], secndNode[1])], "#ffffff", random.randint(0,10))


im.save("op-af.jpg")

# while True:
#     rx1 = random.randint(0, size[0])
#     ry1 = random.randint(0, size[1])
#     rx2 = rx1+boxsize
#     ry2 = ry1+boxsize
#     draw.rectangle([(rx1, ry1), (rx2, ry2)], '#000000')
#     time.sleep(0.5)
#     im.save("this.jpg")
# im.rotate(45).show()
