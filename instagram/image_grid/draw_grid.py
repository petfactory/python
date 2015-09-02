from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import math

page_width = 512
page_height = 512

img_width = 128
img_height = 128
img_half_width = img_width*.5
img_half_height = img_height*.5

num_col = 2
num_row = 2

num_img = 4

img_pivot_spacing_x = 200
img_pivot_spacing_y = 200

offset_x = 0
offset_y = -20

protrusion_x = (page_width - ((num_col-1) * img_pivot_spacing_x)) *.5 + offset_x
protrusion_y = (page_height - ((num_row-1) * img_pivot_spacing_y)) *.5 + offset_y
print(protrusion_x)


pos_list = []
for x in range(num_img):
    col = x % num_col
    row = x / num_row
    #print(col, row)

    x = col * img_pivot_spacing_x + protrusion_x
    y = row * img_pivot_spacing_y + protrusion_y
    print(x, y)
    pos_list.append((x,y))



with Drawing() as draw:


    for p in pos_list:
        x, y = p
        #draw.point(x, y)
        left = x-img_half_width
        top = y-img_half_height
        right = x+img_half_width
        bottom = y+img_half_height

        draw.fill_color = Color('lightblue')
        draw.stroke_color = Color('black')
        draw.stroke_width = 4
        draw.rectangle(left, top, right, bottom)

    with Image(width=page_width, height=page_height, background=Color('lightblue')) as image:
        draw(image)
        image.format = 'jpeg'
        image.save(filename='img_grid.jpg')
