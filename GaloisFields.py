from operator import xor
from functools import reduce

def primeInInterval(N):
    primeNbrs = list(range(2,N))
    i=0
    while i < len(primeNbrs):
        primeNbrs = list(set.difference(set(primeNbrs),set(filter(lambda x : x%primeNbrs[i]==0 if primeNbrs[i] != x else False, primeNbrs))))
        primeNbrs.sort()
        i+=1
    return primeNbrs

#number of galois field with card <= N
def GFInInterval(N):
    gf=set()
    for i in primeInInterval(N):
        tmp=i
        while tmp < N:
            gf.add(tmp)
            tmp*=i
    return gf

N=300
#print(len(GFInInterval(N)))

def multbyalpha(b,f):
    result = b
    h_order_b_position = 0
    while f>>h_order_b_position != 0:
        h_order_b_position+=1
    mask = 2**(h_order_b_position-1)-1
    overflow = mask&f

    result<<=1
    if result > mask:
        result&=mask
        result^=overflow
    return result 
res=1
for i in range(8):
    print(res)
    res=multbyalpha(res,11)

#representation avec une liste
def sum(a,b):
    return list(map(xor, a,b))
b=[1,1,1,0,1]
y=[0,1,1,1,1]
print(sum(b,y))

recompose_nbr = lambda x : reduce(lambda a,b: 2*a+b, x)
def decompose_nbr(x):
    res=[]
    while x>0:
        res.append(x&1)
        x>>=1
    res.reverse()
    return res
