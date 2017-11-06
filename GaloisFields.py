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
print(len(GFInInterval(N)))
