from PIL import Image

size = [7680, 2160]
im = Image.new("RGBA", size, "#000000")
im.save("op.jpg")
