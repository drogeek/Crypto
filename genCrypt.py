#!/bin/python3

import sys

if len(sys.argv) < 2:
	print("missing argument")
	sys.exit()

G=[0b0111000, 0b1010100,0b1100010, 0b1110001]
H=[0b1000111, 0b101011, 0b0011101]

def codage(nbr):
	"""compute Hamming code of a 4 bit number"""
	mask=1
	result=0
	for index in range(len(G)):
		if ((mask<<index)&nbr) != 0:
			result^=G[len(G)-index-1]
	return result
			
with open(sys.argv[1]) as img:
	with open("enc_"+sys.argv[1],"w+") as enc_img:
		#extract and write the 3 first lines
		for i in range(1,4):
			enc_img.write(next(img))
		#calculate Hamming code for every byte cut in two equal parts
		for line in img:
			for number in map(int,line.rstrip().split()):
				enc_img.write(str(codage((number&0b11110000)>>4))+' ')
				enc_img.write(str(codage(number&0b00001111))+' ')
			enc_img.write('\n')
