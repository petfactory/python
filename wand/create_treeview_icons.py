from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

icon_dict = {   'test':[(10, 10), (24, 38), (10, 38)],
                'apa':[(0, 24), (48, 24)],
            }

def create_icons(icon_dict):

    for image_name, point_list in icon_dict.iteritems():

        with Drawing() as draw:
            
            draw.stroke_width = 1
            draw.stroke_color = Color('#999')
            #draw.fill_color = Color('#000')
            draw.fill_opacity = 0
            
            points = point_list
            draw.polyline(points)

            with Image(width=48, height=48) as img:
                draw(img)
                img.format = 'png'
                img.save(filename='icons/{}.png'.format(image_name))


create_icons(icon_dict)