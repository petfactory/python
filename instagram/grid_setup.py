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
                pivot_spacing_x,
                pivot_spacing_y,
                margin):

    page_width_margin = page_width + margin*2
    page_height_margin = page_height + margin*2

    protrusion_x = (page_width_margin - ((num_col-1) * pivot_spacing_x)) *.5 + offset_x
    protrusion_y = (page_height_margin - ((num_row-1) * pivot_spacing_y)) *.5 + offset_y


    num_img = len(image_size_list)

    rect_list = []
    pivot_list = []
    for i in range(num_img):
        col = i % num_col
        row = i / num_row
        #print(col, row)

        # calculate the center pivot for the image grid
        x = col * pivot_spacing_x + protrusion_x
        y = row * pivot_spacing_y + protrusion_y
        #print(x, y)
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

    return rect_list


def test_layout(pivot_spacing_x, pivot_spacing_y, size, num=4, num_col=2, num_row=2):

    #img_width = 100
    #img_height = 100
    #size = (img_width, img_height)
    usize = (size, size)

    #image_size_list = [usize,usize,usize,usize]
    image_size_list = [usize for x in range(num)]

    #image_size_list = [(130,130), (90,120), (120,90), (100, 90)]

    page_width = 500
    page_height = 500

    #pivot_spacing_x = 250
    #pivot_spacing_y = 250

    offset_x = 0
    offset_y = 0

    #num_col = 2
    #num_row = 2

    margin = 0

    return get_img_pos( image_size_list,
                        page_width,
                        page_height,
                        num_col,
                        num_row,
                        offset_x,
                        offset_y,
                        pivot_spacing_x,
                        pivot_spacing_y,
                        margin)



#pivot_spacing_x = 250
#test_layout(pivot_spacing_x)