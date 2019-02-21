from PIL import Image

size = [10000, 10000]
im = Image.new("RGB", size, "#ffffff")
im.save("op.jpg")

# draw = ImageDraw.Draw(im)
#
# boxsize = 6
#
# while True:
#     rx1 = random.randint(0, size[0])
#     ry1 = random.randint(0, size[1])
#     rx2 = rx1+boxsize
#     ry2 = ry1+boxsize
#     draw.rectangle([(rx1, ry1), (rx2, ry2)], '#000000')
#     time.sleep(0.5)
#     im.save("this.jpg")

# im.rotate(45).show()
