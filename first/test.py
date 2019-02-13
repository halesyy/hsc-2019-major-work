from PIL import Image, ImageDraw
import random, time

size = [1920, 1080]
im = Image.open("this.jpg")
# im = Image.new("RGB", size, "#ffffff")

draw = ImageDraw.Draw(im)

boxsize = 6

while True:
    rx1 = random.randint(0, size[0])
    ry1 = random.randint(0, size[1])
    rx2 = rx1+boxsize
    ry2 = ry1+boxsize
    draw.rectangle([(rx1, ry1), (rx2, ry2)], '#000000')
    time.sleep(0.5)
    im.save("this.jpg")

# im.rotate(45).show()
