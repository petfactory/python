#from os import listdir
#from os.path import isfile, join
import sys, os
import re


def get_files(path, pattern):

	dirCont = os.listdir(path)
	min = max = inc = 0
	frameNumList = []
	matchList = []
	for index, cont in enumerate(dirCont):
		
		if os.path.isfile(os.path.join(path, cont)):

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




path = '/Users/johan/Desktop/test'
pattern = re.compile('^test_([\d]*).png$')
get_files(path, pattern)