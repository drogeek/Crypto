#!/bin/python3
import sys
import random as ran
import itertools as ite

if len(sys.argv)<2:
	print("Missing argument")
	sys.exit()

with open(sys.argv[1]) as image:
	with open("e_"+sys.argv[1],"w+") as err_image:
		#writting and skipping the 3 first lines
		for i in range(1,4):
			err_image.write(next(image))
		#extracting string of numbers and converting it to numbers
		numbers = []
		for line in image:
		 	numbers.append(
					list(map(int,filter(lambda x: x!='',line.rstrip().split(' '))))
					)
		#changing one random bit and writting it to the new file
		for line in numbers:
			for pix in line:
				decal=ran.randint(0,7)
				err_image.write(str(pix^(1<<decal))+' ')
			err_image.write('\n')
