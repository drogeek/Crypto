from tables_des import sBox,P,E,IP
from itertools import product, repeat, starmap
from operator import xor
from des import DES

correspondance_messages_encryptions = ( 
(0xef6b0deebd3cd2f5 , 0xaf6b1defe93c93e5),
(0xe043297aeb7383fe , 0xb012397faa2282bb),
(0x9896ad0cb0dd7c3c , 0x8dd6e958b19d7c29),
(0x2702e3f8a51fc06c , 0x7242b7bdb41f8169),
(0x3aa85ac87dca8de3 , 0x6be95fd8389fccb7),
(0x9613b7e714a7d7ed , 0x9203b7b311e2d6f8),
(0x0a604f9d1d678bfc , 0x5b214fd80822cebd),
(0xb6dbaf82da4909a1 , 0xf7cfaad3da184db1),
(0x1c13fdda4016fe02 , 0x1946e9cb1553af06),
(0xdc26ed238d818d56 , 0x9926bd368d81d957)
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

#we verify the result
identity=lambda x : [x]
for key_found in result:
    assert(all(starmap(lambda m,c: DES(m,key_found,compute_ki=identity).C == c, correspondance_messages_encryptions)))

if len(result) == 1:
    print("The key is {}".format(hex(list(result)[0])))
else:
    print("Not enough (message,cypher) to determine with certitude which key it was")
    print("the possible keys are:")
    print(tuple(map(format, result, repeat('0x'))))


