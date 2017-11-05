from tables_des import sBox,P,E,IP
from itertools import product, repeat
from operator import xor

correspondance_messages_encryptions = ( 
(0xef6b0deebd3cd2f5 , 0xef6f4debf838d3b4),
(0xe043297aeb7383fe , 0xe056286bbb2287af),
(0x9896ad0cb0dd7c3c , 0xdc92ad5ca18d7928),
(0x2702e3f8a51fc06c , 0x3342a6a8f51fd439),
(0x3aa85ac87dca8de3 , 0x6aed1bdd78cbd8b2),
(0x9613b7e714a7d7ed , 0x8707e6b711e6c2ad),
(0x0a604f9d1d678bfc , 0x1a210acd4972dab9),
(0xb6dbaf82da4909a1 , 0xb2cbead78b1c4de4),
(0x1c13fdda4016fe02 , 0x5d06a8ce0502bf42),
(0xdc26ed238d818d56 , 0x9d62f8339d95cd07)
)
def reverse_sBox(n,y):
    possible_index = map(lambda i : i.index(y), zip(*[iter(sBox[n])]*16))
    res=[]
    for row,column in enumerate(possible_index):
        tmp=0
        tmp |= column<<1
        tmp |= row&1
        tmp |= (row&2)<<4
        res.append(tmp)
    return res

def reverse_perm(p):
    tmp=[0]*len(p)
    for i,e in enumerate(p):
        tmp[e-1] = i + 1
    return tmp
P_inv = reverse_perm(P)
assert(all([ P_inv[P[i]-1]-1 == i for i in range(len(P)) ]))

MASK32=2**32-1
MASK4=2**4-1
#we try to determine the common key, from different input and output on one turn of DES
def reverse_S(e,o):
    Re, Le = e&MASK32, e>>32
    Ro, Lo = o&MASK32, o>>32
    assert(Lo == Re)
    output_f = Ro^Le

    output_sBox = 0
    for i,shift in enumerate(P_inv):
        output_sBox |= ((output_f>>(shift-1))&1)<<i

    possibilities = []
    for i in range(8):
       tmp = (output_sBox >> (i*4)) & MASK4
       possibilities.append(reverse_sBox(i,tmp))

    return tuple(product(*possibilities))

def reconstruct_number(coeffs, bits):
    y = 0
    for i, coeff in enumerate(coeffs):
        y |= coeff << (i*bits)
    return y
reconstruct_number_test = [MASK4]*3
reconstruct_number_test[2]=MASK4-2

tmp=[]
for m_perm,c_perm in correspondance_messages_encryptions:
    m,c = 0,0
    #we apply the initial permutation to the message and cypher
    for i,ip in enumerate(IP):
      m |= (((m_perm >> (ip -1)) & 1) << i)
      c |= (((c_perm >> (ip -1)) & 1) << i)
    
    #we reverse L and R
    c = ((c&MASK32) << 32) | (c >> 32)
    Re = m&MASK32
    expanded_input = 0 
    for index,shift in enumerate(E):
        expanded_input |= ((Re>>(shift-1))&1)<<index

    coeffs = reverse_S(m,c)
    reconstructed_nbrs = map(reconstruct_number, coeffs, repeat(6))
    possible_keys = map(xor, reconstructed_nbrs, repeat(expanded_input))
    tmp.append(set(possible_keys))

result = set.intersection(*tmp)
print(list(map(format,result, repeat('0x'))))
