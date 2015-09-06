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


thumbnail('/Users/johan/Desktop/pics', 64, 64)
