from PIL import Image, ImageDraw
import random, time

size = [1920, 1080]
im = Image.open("op.jpg")
draw = ImageDraw.Draw(im)

nodeAmount = 3
nodeStorage = []

#/ First, generate the nodes coords.
for i in range(0, nodeAmount):
    nodeStorage[i] = [random.randint(0, size[0]), random.randit(0, size[1])]
    print(nodeStorage)



# while True:
#     rx1 = random.randint(0, size[0])
#     ry1 = random.randint(0, size[1])
#     rx2 = rx1+boxsize
#     ry2 = ry1+boxsize
#     draw.rectangle([(rx1, ry1), (rx2, ry2)], '#000000')
#     time.sleep(0.5)
#     im.save("this.jpg")
# im.rotate(45).show()
