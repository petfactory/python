from wand.image import Image
from wand.drawing import Drawing
import os
import shutil
import pprint

def make_thumbs():

    img = Image(filename='square.jpg')
    w, h = img.size

    with Drawing() as draw:
        draw.line((0, 0), (w, h))
        draw.line((0, h), (w , 0))
        draw(img)

    img.format = 'jpeg'
    img.save(filename='off_square.jpg')

make_thumbs()
