from PIL import Image

import sys

image_path = sys.argv[1]
print(image_path)

image = Image.open(image_path)
loaded = image.load()
width, height = image.size
output = []
for x in range(width):
    for y in range(height):
        if loaded[x, y] != (0, 0, 0, 0):
            output.append((x,-y))

print(output)