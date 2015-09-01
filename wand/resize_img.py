from wand.image import Image
import os
import shutil
import pprint

def make_thumbs(source_dir, thumb_dir, thumb_size, thumb_format):

	if os.path.isdir(thumb_dir):
		print('delete dir')
		#input('12')
		shutil.rmtree(thumb_dir)

	os.makedirs(thumb_dir)

	for index, file_name in enumerate(os.listdir(source_dir)):

		img_name, file_ext = os.path.splitext(file_name)
		if file_ext not in ('.jpg', '.jpeg'):
			continue

		img = Image(filename=os.path.join(source_dir, file_name))
		img.resize(thumb_size, thumb_size)

		img.format = thumb_format
		img.save(filename=os.path.join(thumb_dir, '{}_thumb.{}'.format(img_name, thumb_format)))

source_dir = 'pics'
thumb_dir = r'thumbs'
thumb_size = 64
thumb_format = 'jpeg'

make_thumbs(source_dir, thumb_dir, thumb_size, thumb_format)
