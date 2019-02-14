from PIL import Image

size = [10000, 10000]
im = Image.new("RGB", size, "#000000")
im.save("op.jpg")
