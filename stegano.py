import sys
from operator import mul
from functools import reduce
from itertools import chain

def bin_decomp(string):
	for char in string:
		mask=1
		for i in range(8):
			yield (ord(char)&mask)>>i
			mask<<=1
if len(sys.argv) < 3:
	print("missing argument")
	sys.exit()

str_to_encapsulate = sys.argv[2]
with open(sys.argv[1]) as img:
	img.readline()
	available_bits = reduce(mul,map(int,img.readline().split(' ')))
	img.readline()
	if len(str_to_encapsulate)*8 > available_bits:
		print("message too long, only {} characters available in this image".format(available_bits//8))
		sys.exit()
#each bit from the string to encode along with each number representing each pixel in the image
	for bit,pix in zip(bin_decomp(str_to_encapsulate),map(int,chain.from_iterable(map(lambda x: x.strip().split(),img.readlines())))):
		print(pix^bit)
