from tables_des import *
from functools import reduce
from itertools import product,starmap,repeat,islice

verif_S = {0x8b8e5abecc6d : 0xb06083b1, 0xce5283e393ca : 0xcd2b5bef, 0xe8c81f1e2171 : 0x38965645, 0xa318b0c9dac2 : 0x99ef1ff4, 0xeac70a17bb02 : 0x375ab5d4}
def sbox(n,a):
# renvoie pour une entree a de 6 bits, la sortie de la boite numero n
  f_bit=1
  l_bit=2**5
  m_bits=(2**4-1)*2
  line=(a&l_bit)>>4 | a&f_bit
  column=(a&m_bits)>>1
#print("line={},column={}".format(line,column))
  return sBox[n][16*line+column]
#print(sbox(1,0x31))
def S(x):
# x est un mot de 48 bits et cette fonction renvoie les 32 bits obtenus apres application
# de 8 boites S sur x
  result = 0
  i = 0 
  mask=0x3f
  while i < 8:
#   print("mask="+format((x&mask)>>(i*6),'0x'))
#   print("sbox="+format(sbox(i,(x&mask)>>(i*6)),'0x'))
    result+=sbox(i,(x&mask)>>(i*6))<<(i*4)
    mask<<=6
    i+=1
  return result
assert(all(map(lambda x: verif_S[x]==S(x),verif_S)))

def CalculKi(K):

#attention C et D doivent etre consideres stockes que sur 28 bits 

  
  def shrick_perm(x, shrick_perm_list):
    res=0
    for i,shift in enumerate(shrick_perm_list):
        res |= ((x>>(shift-1))&1)<<i
    return res

  # Application de la permutation PC1 sur la cle K
  # le resultat est stocke dans PC1K
  PC1K = shrick_perm(K,PC1)
  C = (PC1K >> 28) & MASK28 
  D = PC1K & MASK28

  # Calcul des 16 cles intermediaires

  def circular_shift(shift,nbr):
    nbr = nbr << shift
    overflow = nbr >> 28
    nbr = (nbr&MASK28) | overflow
    return nbr

  #didn't find out how to do that in a functional way
  shifted_Cs = [C]
  shifted_Ds = [D]
  for shift in LS:
    shifted_Cs.append(circular_shift(shift,shifted_Cs[-1]))
    shifted_Ds.append(circular_shift(shift,shifted_Ds[-1]))

  combined_keys = starmap(lambda C,D: (C<<28) | D, zip(shifted_Cs,shifted_Ds))
  #print(list(map(lambda x : format(x,'0x'), combined_keys)))

  # Application de la permutation PC2
  next(combined_keys)
  ki = tuple(map(shrick_perm, combined_keys, repeat(PC2)))
  return(ki)

MASK6 = 0x3f
MASK28 = 0xfffffff
MASK32 = 0xffffffff
K=0x1123456789abcdef
M=0xaaaabbbbccccdddd

Ki = CalculKi(K)
print(tuple(map(lambda x : format(x,'0x'), Ki)))


#Application de la Permutation IP sur le message M 
# le resultat est stocke dans tempo

tempo = 0
for i,ip in enumerate(IP):
      tempo |= (((M >> (ip -1)) & 1) << i)

#les 16 tours du DES 
L = (tempo >> 32) 
R = tempo & MASK32 

for subkey in Ki:
  Z = L 
  L = R 

  # expansion de R via la table E
  # resultat stocke dans tempo 
  tempo = 0 
  for index,shift in enumerate(E):
    tempo |= ((R>>(shift-1))&1)<<index

  # ajout de la clef de tour
  tempo ^= subkey

  # action des boites S
  tempo = S(tempo);

  # Application de la permutation P sur tempo
  # on stocke le resultat dans R
  R = 0 
  for index,shift in enumerate(P):
    R |= ((tempo>>(shift-1))&1)<<index
  R ^= Z 
  i = i + 1

# echange final entre R et L
T = R<<32
T |= L

# Application de la Permutation IP^-1 sur (R16L16)
# le resultat est stocke dans C
C = 0
for index, shift in enumerate(InvIP):
    C |= ((T>>(shift-1))&1)<<index
print("Crypto = ",hex(C))
