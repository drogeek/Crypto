import sys
from operator import mul
from functools import reduce
from itertools import chain
from math import log, ceil

def bin_decomp_str(string):
	for char in string:
		mask=1
		for i in range(8):
			yield (ord(char)&mask)>>i
			mask<<=1
def bin_decomp(nbr):
  while nbr>0:
    yield nbr&1
    nbr>>=1

if len(sys.argv) < 3:
	print("missing argument")
	sys.exit()

str_to_encapsulate = sys.argv[2]
with open(sys.argv[1]) as img:
  with open('{}_stegano.pgm'.format(''.join(sys.argv[1].split('.')[0])),'w') as output_img:
    output_img.write(img.readline())
    nbr_pix_line = img.readline()
    output_img.write(nbr_pix_line)
    available_bits = reduce(mul,map(int,nbr_pix_line.split(' ')))
#the number of bits necessary to code the size of the hidden message in the image
    bit_nbr_msg_size = ceil(log(available_bits,2))
    print(bit_nbr_msg_size)
    size_msg = len(str_to_encapsulate)*8 
#binary representation of size_msg from less to most representative bit
    size_msg_bin = list(bin_decomp(size_msg))
    size_msg_bin.reverse()
    size_msg_bin_padding = [0]*(bit_nbr_msg_size-len(size_msg_bin)) + size_msg_bin

    output_img.write(img.readline())
    if size_msg + bit_nbr_msg_size > available_bits:
      print("message too long, only {} characters available in this image".format((available_bits-bit_nbr_msg_size)//8))
      sys.exit()
    pixels_str=list(chain.from_iterable(map(lambda x: x.strip().split(),img.readlines())))
#each bit from the string to encode along with each number representing each pixel in the image
    for index,(bit,pix) in enumerate(zip(chain(size_msg_bin_padding, bin_decomp_str(str_to_encapsulate)),map(int,pixels_str))):
      print(bit)
      pixels_str[index]=str(pix^bit)
    output_img.write(' '.join(pixels_str))
