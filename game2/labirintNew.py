from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsTextItem

import numpy as np

def pos(x,y,h,w):
    return x*w+y+2*(h+1)*(w+1)-h-w-1

def check(string,n):
    if len(string)>10: return False
    var = list(map(str,range(1,n+1)))
    for e in string:
        if e not in var: return False
    return True

def BFS(self,x,y,z):
    n = 0
    maze = np.zeros([4,self.hL,self.wL])
    S1 = [(x,y,z)]
    S2 = []
    while len(S1)>0:
        n+=1
        for i in range(len(S1)):
            x,y,z = S1.pop()
            if [x,y,z]==self.exit: return n-1
            if maze[z][x][y]==0:
                maze[z][x][y] = n
                for i in range(self.N+2):
                    t = 1-self.Lab[x+(1-z%2)*(z//2)][y+(z%2)*(z//2)][z%2]
                    x1,y1,z1 = self.func[i](x,y,z,t)
                    if (0<=x1<self.hL and 0<=y1<self.wL
                        and maze[z1][x1][y1] == 0):
                        S2.append((x1,y1,z1))
        S1,S2 = S2,S1
    return -1

def TIP(self,t):
    tip = dict()
    tip[BFS(self,*self.xyz)] = [(-1,0),(-1,0)]
    a,b = self.var
    if a == self.N+2:
        if b == self.N+2:
            for i in range(self.N+2):
                jocker(self,i,tip,i)
        else:
            jocker(self,b,tip)
    elif b == self.N+2:
        jocker(self,a,tip)
    else:
        tree2(self,a,b,tip)
        tree1(self,a,2,tip)
        tree1(self,b,2,tip)

    self.tip = min(tip.keys())
    if self.tip<0:
        print("no exit")
        return [-1,-1]
    self.tip = tip[self.tip]
    tip = ["-","-"]
    if self.tip[0][0]!=-1:
        tip[0] = self.icons[self.tip[0][0]]
        if self.tip[0][1]>1:
            tip[0] += '('+str(self.tip[0][1])+')'
    if self.tip[1][0]!=-1:
        tip[1] = self.icons[self.tip[1][0]]
        if self.tip[1][1]>1:
            tip[1] += '('+str(self.tip[1][1])+')'
    if t: print("(",*tip,")",end = " ")
    return tip

def jocker(self,i,tip,k=0):
    for j in range(k,self.N+2):
        tree2(self,i,j,tip)
        tree1(self,j,1,tip)
    tree1(self,i,6,tip)
    return None

def tree1(self,i,n,tip):
    x,y,z = self.xyz
    for k in range(n):
        t = 1-self.Lab[x+(1-z%2)*(z//2)][y+(z%2)*(z//2)][z%2]
        x,y,z = self.func[i](x,y,z,t)
        if 0<=x<self.hL and 0<=y<self.wL:
            t = BFS(self,x,y,z)
            if tip.get(t,0) == 0: tip[t] = [(i,k+1),(-1,0)]
        else: return None
    return None

def tree2(self,i,j,tip):
    x,y,z = self.xyz
    t = 1-self.Lab[x+(1-z%2)*(z//2)][y+(z%2)*(z//2)][z%2]
    x,y,z = self.func[i](x,y,z,t)
    if 0<=x<self.hL and 0<=y<self.wL:
        t = 1-self.Lab[x+(1-z%2)*(z//2)][y+(z%2)*(z//2)][z%2]
        x,y,z = self.func[j](x,y,z,t)
        if 0<=x<self.hL and 0<=y<self.wL:
            t = BFS(self,x,y,z)
            if tip.get(t,0) == 0: tip[t] = [(i,1),(j,1)]
    if i!=j:
        x,y,z = self.xyz
        t = 1-self.Lab[x+(1-z%2)*(z//2)][y+(z%2)*(z//2)][z%2]
        x,y,z = self.func[j](x,y,z,t)
        if 0<=x<self.hL and 0<=y<self.wL:
            t = 1-self.Lab[x+(1-z%2)*(z//2)][y+(z%2)*(z//2)][z%2]
            x,y,z = self.func[i](x,y,z,t)
            if 0<=x<self.hL and 0<=y<self.wL:
                t = BFS(self,x,y,z)
                if tip.get(t,0) == 0: tip[t] = [(j,1),(i,1)]
    return None

