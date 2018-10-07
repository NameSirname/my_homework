import numpy as np
from numpy import random as rnd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation
from time import *


n,a = 199,1
##B = [[4]*(n+2)]+[[4]+[rnd.randint(0,4) for i in range(n)]+[4] for j in range(n)]+[[4]*(n+2)]
B = [[np.NaN]*(n+2)]+[[np.NaN]+[a for i in range(n)]+[np.NaN] for j in range(n)]+[[np.NaN]*(n+2)]
##B = [[4]*(n+2)]+[[4]+[a for i in range(n)]+[4] for j in range(n)]+[[4]*(n+2)]
A = np.array(B)#, dtype=int)

def visualize():
    plt.close()
    fig1 = plt.figure()
    fig1.add_subplot(111)
    ax1 = plt.imshow(A,vmin=0,vmax=4)

    bounds = np.linspace(0, 4, 5)
    cbar = plt.colorbar(ticks=bounds)

    cmap = mpl.cm.get_cmap('hot',5)
    plt.set_cmap(cmap)

    plt.show(block=False)
    return None

print(ctime())

a,b = (n+1)//2,(n+1)//2
S1=set()
S2=set()
def sand(a,b):
    global S1, S2, A
    A[a][b]+=1
    if A[a][b]>=4:
        S1.add((a,b))
    while len(S1)>0 or len(S2)>0:
        while len(S1)>0:
            s = S1.pop()
            a,b = s[0],s[1]
            A[a+1][b]+=A[a][b]//4
            if A[a+1][b]>=4: 
                S2.add((a+1,b))
            A[a-1][b]+=A[a][b]//4
            if A[a-1][b]>=4:
                S2.add((a-1,b))
            A[a][b+1]+=A[a][b]//4
            if A[a][b+1]>=4:
                S2.add((a,b+1))
            A[a][b-1]+=A[a][b]//4
            if A[a][b-1]>=4:
                S2.add((a,b-1))
                
            A[a][b]%=4

        S1=S2.copy()
        S2.clear()
    
c=0
for e in range(100000):
    sand(a,b)
    c+=1
    print(c, end='\t')
    if c%100==0:
        visualize()
print(ctime())




