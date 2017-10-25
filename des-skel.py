from tables_des import *

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

  PC1K = 0
  ki = [0]*16
  i = 0 

  def decomp_bit(x):
    while x>0:
      yield x&1
      x>>=1

  # Application de la permutation PC1 sur la cle K
  # le resultat est stocke dans PC1K
  K_decomp=list(decomp_bit(K))
  for power,bit in enumerate(( K_decomp[i] for i in PC1 )):
    PC1K+=bit*2**power

  C = (PC1K >> 28) & MASK28 
  D = PC1K & MASK28 ;
  i = 0
  # Calcul des 16 cles intermediaires
  while (i < 16):
      # Application du shift circulaire  sur C et D
      # A COMPLETER
      tempo = (C << 28) | D;
      ki[i] = 0;
      j = 0
      # Application de la permutation PC2 sur tempo afin d'obtenir la cle de tour numero i
      # le resultat est stocke dans ki[i]
      while (j < 48):
        break
          # A COMPLETER
      i = i + 1
  return(ki)

MASK6 = 0x3f
MASK28 = 0xfffffff
MASK32 = 0xffffffff
K=0x1123456789abcdef
M=0xaaaabbbbccccdddd

Ki = CalculKi(K);


#Application de la Permutation IP sur le message M 
# le resultat est stocke dans tempo

tempo = 0
i = 0
while i < 64:
      tempo |= (((M >> (IP[i] -1)) & 1) << i)
      i = i + 1

#les 16 tours du DES 
L = (tempo >> 32) 
R = tempo & MASK32 
i = 0
while i < 16 :
  Z = L 
  L = R 

  # expansion de R via la table E
  # resultat stocke dans tempo 
  tempo = 0 
  j = 0
  while j < 48:
    break
    # A COMPLETER

  # ajout de la clef de tour
  tempo ^= Ki[i] 

  # action des boites S
#tempo = S(tempo);

  # Application de la permutation P sur tempo
  # on stocke le resultat dans R
  R = 0 
  j = 0
  while j < 32:
    break
      # A COMPLETER
  R ^= Z 
  i = i + 1

# echange final entre R et L
# A COMPLETER

# Application de la Permutation IP^-1 sur (R16L16)
# le resultat est stocke dans C
C = 0
i = 0 
while i < 64:
  break
  # A COMPLETER
print("Crypto = ",hex(C))
