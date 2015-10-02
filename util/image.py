from wand.image import Image
import os
import shutil
import pprint
import datetime

def thumbnail(source_dir, width, height, thumb_format='jpeg'):

    if not os.path.isdir(source_dir):
        print('the directory does not exist')
        return

    dt = datetime.datetime.today()
    dtstring =  dt.strftime("%Y-%m-%d %H-%M-%S")

    dest_dir = os.path.join(source_dir, 'thumbs {}'.format(dtstring))
    os.makedirs(dest_dir)

    
    for index, file_name in enumerate(os.listdir(source_dir)):

        img_name, file_ext = os.path.splitext(file_name)
        if file_ext not in ('.jpg', '.jpeg', '.png'):
            continue

        img = Image(filename=os.path.join(source_dir, file_name))
        img.resize(width, height)

        img.format = thumb_format
        img.save(filename=os.path.join(dest_dir, '{}_thumb.{}'.format(img_name, thumb_format)))


#thumbnail('/Users/johan/Desktop/pics', 128, 128)

def appicon(source_image, dest_dir, size_dict):

    if not os.path.isdir(dest_dir):
        print('the directory does not exist')
        return

    name = size_dict.get('name')
    size_dict = size_dict.get('sizes')

    dt = datetime.datetime.today()
    dtstring =  dt.strftime("%Y-%m-%d %H-%M-%S")

    dest_dir = os.path.join(dest_dir, '{}_{}'.format(name, dtstring))
    os.makedirs(dest_dir)

    img_name, file_ext = os.path.splitext(source_image)
    if file_ext not in ('.jpg', '.jpeg', '.png'):
        return

    for name, size in size_dict.iteritems():

        img = Image(filename=source_image)
        img.resize(size, size)

        img.format = 'png'
        img.save(filename=os.path.join(dest_dir, '{}.png'.format(name)))

size_dict_mac = {   'name':'mac',
                    'sizes':{   'icon_512x512@2x':1024,
                                'icon_512x512':512,
                                'icon_256x256@2x':512,
                                'icon_256x256':256,
                                'icon_128x128@2x':256,
                                'icon_128x128':128,

                                'icon_32x32@2x':64,
                                'icon_32x32':32,
                                'icon_16x16@2x':32,
                                'icon_16x16':16
                            }
                }

size_dict_iphone = {   'name':'iphone',
                        'sizes':{   '29pt@2x':58,
                                    '29pt@3x':87,
                                    '40pt@2x':80,
                                    '40pt@3x':120,
                                    '60pt@2x':120,
                                    '60pt@3x':180,

                            }
                }


appicon(source_image='/Users/johan/Desktop/mmmPuss/mmmPuss.png',
        dest_dir='/Users/johan/Desktop/mmmPuss',
        size_dict = size_dict_iphone)

