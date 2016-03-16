from wand.image import Image
import os
import shutil
import pprint

def resave_png(source_dir):

    dest_dir = os.path.join(source_dir, 'new')

    if os.path.isdir(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)


    for index, file_name in enumerate(os.listdir(source_dir)):

        img_name, file_ext = os.path.splitext(file_name)
        print file_ext

        if file_ext not in ['.png']:
            #print ('apapap', file_name)
            continue

        #print os.path.join(source_dir, file_name)
        with Image(filename=os.path.join(source_dir, file_name)) as original:
            with original.convert('png') as converted:
                converted.save(filename=os.path.join(dest_dir, file_name))
                #pass


resave_png(source_dir='/Users/johan/desktop/rc')