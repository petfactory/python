from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from PySide import QtCore

def get_img_pos(image_size_list,
                page_width,
                page_height,
                num_col,
                num_row,
                offset_x,
                offset_y,
                img_pivot_spacing_x,
                img_pivot_spacing_y,
                margin):

    #protrusion_x = (page_width - ((num_col-1) * img_pivot_spacing_x)) *.5 + offset_x
    #protrusion_y = (page_height - ((num_row-1) * img_pivot_spacing_y)) *.5 + offset_y
    page_width_margin = page_width + margin*2
    page_height_margin = page_height + margin*2

    protrusion_x = (page_width_margin - ((num_col-1) * img_pivot_spacing_x)) *.5 + offset_x
    protrusion_y = (page_height_margin - ((num_row-1) * img_pivot_spacing_y)) *.5 + offset_y


    num_img = len(image_size_list)

    rect_list = []
    pivot_list = []
    for i in range(num_img):
        col = i % num_col
        row = i / num_row
        #print(col, row)

        # calculate the center pivot for the image grid
        x = col * img_pivot_spacing_x + protrusion_x
        y = row * img_pivot_spacing_y + protrusion_y
        print(x, y)
        #pos_list.append((x,y))

        width = image_size_list[i][0]
        height = image_size_list[i][1]
        left = x-width*.5
        top = y-height*.5

        #print('l: {}   t: {}   w: {}   h: {}'.format(left, top, width, height))

        rect = QtCore.QRect(left, top, width, height)
        #print(rect)
        rect_list.append(rect)
        pivot_list.append((x,y))


    # debug render
    with Drawing() as draw:

        draw.fill_color = Color('lightblue')
        draw.stroke_color = Color('#999')
        draw.stroke_width = 1

        # margin
        draw.rectangle(margin, margin, page_width+margin, page_height+margin)

        
        # page center
        draw.line((page_width_margin*.5, 0), (page_width_margin*.5, page_height_margin))
        draw.line((0, page_height_margin*.5), (page_width_margin, page_height_margin*.5))

        draw.stroke_color = Color('black')
        draw.stroke_width = 2

        for rect in rect_list:
            draw.rectangle(rect.left(), rect.top(), rect.left()+rect.width(), rect.top()+rect.height())


        draw.fill_color = Color('black')
        for pivot in pivot_list:
            
            draw.point(pivot[0], pivot[1])

        with Image(width=page_width_margin, height=page_height_margin, background=Color('lightblue')) as image:
            draw(image)
            image.format = 'jpeg'
            image.save(filename='debug_render_grid.jpg')


img_width = 100
img_height = 100
size = (img_width, img_height)
image_size_list = [size,size,size,size]

#image_size_list = [(130,130), (90,120), (120,90), (100, 90)]

page_width = 500
page_height = 500



img_pivot_spacing_x = 250
img_pivot_spacing_y = 250

offset_x = 0
offset_y = 0

num_col = 2
num_row = 2

margin = 20

get_img_pos(image_size_list,
            page_width,
            page_height,
            num_col,
            num_row,
            offset_x,
            offset_y,
            img_pivot_spacing_x,
            img_pivot_spacing_y,
            margin)
