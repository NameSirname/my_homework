def to_gray(n=0):
    n=bin(n)[2:]
    m=n[0]
    for i in range(1,len(n)):
        m+= str((int(n[i])+int(n[i-1]))%2)
    return m

def from_gray(n='0'):
    m=n[0]
    for i in range(1,len(n)):
        m+= m[i-1]*(1-int(n[i]))+ str(1-int(m[i-1]))*int(n[i])
    m=int(m,2)
    return m
        
def g_up(n):
    q,l = len(n),0
    n ='0'+n
    t,k=0,0
    if n[q]=='0':
        t,k=1,1
    for e in range(1,q):
        l+= int(n[q-e])
        if t and n[q-e]=='0':
            k+=1
        else:
            t=0
    l=l%2

    if not l and k:
        n= n[1:-1]+'1'
    elif l and not k:
        n= n[1:-1]+'0'
    else:
        n=n[1:-k-2]+ str(1-int(n[-k-2]))+n[-k-1:]
    return n


def g_down(n):
    q,l = len(n),0
    n ='0'+n
    t,k=0,0
    if n[q]=='0':
        t,k=1,1
    for e in range(1,q):
        l+= int(n[q-e])
        if t and n[q-e]=='0':
            k+=1
        else:
            t=0
    l=l%2

    if l and k:
        n= n[1:-1]+'1'
    elif not l and not k:
        n= n[1:-1]+'0'
    else:
        n=n[1:-k-2]+ str(1-int(n[-k-2]))+n[-k-1:]
    if len(n)>1 and n[0]=='0':
        n=n[1:]
    return n
##
##def zeta(n,a):
##    s=0
##    for i in range(1,n+1):
##        s+= 1/(i**a)
##    return s
##
##alpha3 = 1.202056903150321  ##zeta(1000000,3)
##
##
##def dzeta(n,a):
##    s = ddrob(0,1)
##    for i in range(1,n+1):
##        dx = ddrob(1,i**a)
##        s = ddrob(s.ch*dx.zn+dx.ch*s.zn, s.zn*dx.zn)
##    return s
##
##class ddrob(object):
##    def __init__(self, ch, zn=1):
##        self.ch = ch
##        self.zn = zn
##        self.val = ch / zn
##
##    def nod_d(self, ch, zn):
##        if zn == 0:
##            self.ch = self.ch // ch
##            self.zn = self.zn // ch
##            return None
##        else:
##            ch %= zn
##            return self.nod_d(zn, ch)
##
##    def drob(self):
##        print(self.ch, '/', self.zn, '=', self.base_conv(10))
##
##    ##
##    def base_conv(self, base=10):
##        if base > 10:
##            return 'use base_conv_l'
##
##        num = self.ch // self.zn
##        c = delit(num, base)
##        c += '.'
##
##        dr = self.ch % self.zn
##        zn = self.zn
##        st_e = step_enter(self.zn, base)
##        nd = nod(base, zn // (base ** st_e))
##
##        while nd != 1:
##            zn *= base // nd
##            dr *= base // nd
##            st_e += 1
##            nd = nod(base, zn // (base ** st_e))
##
##        for e in range(st_e):
##            zn //= base
##            c += str(dr // zn)
##            dr = dr % zn
##
##        n = 1
##        while (base ** n - 1) % zn != 0 and n <= zn:
##            n += 1
##
##        dr = dr * (base ** n - 1) // zn
##        dr = delit(dr, base)
##        c = c + '(' + '0' * (n - len(dr)) + dr + ')'
##        return c
