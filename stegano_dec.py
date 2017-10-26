import sys
from operator import mul
from functools import reduce
from itertools import chain
from math import log, ceil

if len(sys.argv) < 2:
	print("missing argument")
	sys.exit()

#requires input from most to less representative bit
to_nbr = lambda x : reduce(lambda a,b: a*2+b, x)

str_to_encapsulate = sys.argv[2]
with open(sys.argv[1]) as img:
    nbr_pix_line = img.readline()
    available_bits = reduce(mul,map(int,nbr_pix_line.split(' ')))
#the number of bits necessary to code the size of the hidden message in the image
    bit_nbr_msg_size = ceil(log(available_bits,2))
    data = img.readline().split()
    size_msg_bin = [ int(data[i])&1 for i in range(bit_nbr_msg_size) ]
    size_msg = to_nbr(size_msg_bin)
    print(size_msg)
    
    msg_bin = [ pix&1 for pix in range(bit_nbr_msg_size,len(data)) ]
    msg_per_byte = zip(*[iter(msg_bin)]*8)
