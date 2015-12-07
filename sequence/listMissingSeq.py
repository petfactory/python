#from os import listdir
#from os.path import isfile, join
import sys, os
import re


def createFiles(dirPath, name, ext, start, end):

	for i in range(start, end+1):
		fileName = '{0}.{1:03d}.{2}'.format(name, i, ext)
		file = open(os.path.join(dirPath, fileName), "w")
		file.close()
		#print(fileName)


def get_files(dirPath, pattern):

	dirCont = os.listdir(dirPath)
	min = max = inc = 0
	frameNumList = []
	matchList = []
	for index, cont in enumerate(dirCont):
		
		if os.path.isfile(os.path.join(dirPath, cont)):

			match = pattern.match(cont)

			if match:
				fullMatch = match.group()
				mGroups = match.groups()
				matchList.append(fullMatch)

				try:
					num = int(mGroups[0])
				except ValueError as e:
					print('The capturing group is not a number!\n{}'.format(e))
					return
				if inc == 0:
					min = num
					max = min
					inc += 1

				if num < min:
					min = num

				elif num > max:
					max = num

				if num not in frameNumList:
					frameNumList.append(num)

	fullSet = set(xrange(min, max + 1))
	diffSet = fullSet.difference(set(frameNumList))
	print('{} Total number of frames'.format((max+1)- min))
	print('{} Missing frames'.format(len(diffSet)))
	print('missing values are :{0}'.format(sorted(diffSet)))

	print('-----------')
	for i in range(min, max+1):
		name = ''
		if i in diffSet:
			name = '-> missing'
		print('{} {}'.format(i, name))
	print('-----------')



dirPath = '/Users/johan/Desktop/testDir'
name = 'robot_lighting'
ext = 'png'

# create some dummy files
createFiles(dirPath, name, ext, start=1, end=10)
createFiles(dirPath, name, ext, start=15, end=20)


# search for missing files
pattern = re.compile('^robot_lighting.([\d]*).png$')
get_files(dirPath, pattern)






