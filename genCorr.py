#!/bin/python3

import sys

if len(sys.argv) < 2:
	print("missing argument")
	sys.exit()

G=[0b0111000, 0b1010100,0b1100010, 0b1110001]
H=[0b1000111, 0b101011, 0b0011101]
#map for syndromes
M=dict(zip(range(1,8),(1<<4,1<<5,1<<3,1<<6,1<<2,1<<1,1)))

def getSyndrome(nbr):
	result = 0
	for index in range(len(H)):
		#computes the binary weight of each product of each line of H with nbr
		#and shifts the result successively to construct the syndrome
		result+=int(bin(H[len(H)-index-1]&nbr).count('1'))%2<<index
	return result

with open(sys.argv[1]) as img:
	with open("cor_"+sys.argv[1],"w+") as cor_img:
		#extract and write the 3 first lines
		for i in range(1,4):
			cor_img.write(next(img))

		#corrects received Hamming message
		#regroups pairs of splited Hamming messages into one
		cpt=0
		for line in img:
			for number in map(int,line.rstrip().split()):
				syndrome = getSyndrome(number)
				if syndrome != 0:
					number^=M[syndrome]
				number&=0b00001111
				if cpt%2 == 0:
					result=number<<len(G)
				else:
					result+=number
					cor_img.write(str(result)+' ')
				cpt+=1
			cor_img.write('\n')
