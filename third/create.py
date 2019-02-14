from PIL import Image

size = [3840, 1080]
im = Image.new("RGB", size, "#000000")
im.save("op.jpg")
