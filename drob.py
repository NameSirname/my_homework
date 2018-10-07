# -*- coding: utf8 -*-

class drob(object):
    def __init__(self, ch, zn=1, i=1):
        if zn==0:
            raise ZeroDivisionError("denominator mustn't be 0")
        self.ch = ch
        self.zn = zn
        if i:
            self.nod_d(self.ch, self.zn)
        self.val = ch / zn
        self._ = str(self.ch)+'/'+str(self.zn)

    def nod_d(self, ch, zn):
        while zn!=0:
            ch%=zn
            zn,ch = ch,zn
            
        self.ch = self.ch // ch
        self.zn = self.zn // ch
        return None
    
    def drob(self):
        print(self.ch, '/', self.zn, '=', self.base_conv())
        
##______________________________________________________________
    def __neg__(self):
        return drob(-self.ch,self.zn,i=0)

    def __pos__(self):
        return self
    
    def __abs__(self):
        return drob(abs(self.ch),self.zn)
    
    def __bool__(self):
        return self.ch!=0
    
    def __str__(self):
        return self._

##________________________________________________________________
    def __add__(self, drob2):
        if isinstance(drob2,(float,int)):
            drob2 = to_drob(drob2)
        if isinstance(drob2,drob):
            return drob(self.ch * drob2.zn + self.zn * drob2.ch,
                        self.zn * drob2.zn)
        else:
            raise TypeError('drob can be multiplied only by drob, int or float')
    
    
    def __sub__(self, drob2):
        if isinstance(drob2,(float,int)):
            drob2 = to_drob(drob2)
        if isinstance(drob2,drob):
            return drob(self.ch * drob2.zn - self.zn * drob2.ch,
                        self.zn * drob2.zn)
        else:
            raise TypeError('drob can be multiplied only by drob, int or float')
    
    def __mul__(self,drob2):
        if isinstance(drob2,(float,int)):
            drob2 = to_drob(drob2)
        if isinstance(drob2,drob):
            return drob(self.ch*drob2.ch, self.zn*drob2.zn)
        else:
            raise TypeError('drob can be multiplied only by drob, int or float')
    
    def __truediv__(self,drob2):
        if isinstance(drob2,(float,int)):
            drob2 = to_drob(drob2)
        if isinstance(drob2,drob):
            return drob(self.ch*drob2.zn, self.zn*drob2.ch)
        else:
            raise TypeError('drob can be divided only by drob, int or float')
    
    def __div__(self,drob2):
        return self.__truediv__(drob2)

    def __pow__(self,val):
        if not isinstance(val,int):
            return self.val**val
            #raise TypeError('value must be integer')
        if val>=0:
            return drob(self.ch**val,self.zn**val, i=0)
        else:
            return drob(self.zn**(-val),self.ch**(-val), i=0)

    def __mod__(self,drob2):
        c = self/drob2
        return self - drob((c.ch//c.zn)*drob2.ch, drob2.zn)

    
    def __floordiv__(self,drob2):
        return (self-self%drob2)/drob2


##___________________________________________________
    def __le__(self, drob2):
        if (self - drob2).ch<=0:
            return True
        else:
            return False
        
    def __lt__(self, drob2):
        if (self - drob2).ch<0:
            return True
        else:
            return False
       
    def __ge__(self, drob2):
        if (self - drob2).ch>=0:
            return True
        else:
            return False

    def __gt__(self, drob2):
        if (self - drob2).ch>0:
            return True
        else:
            return False
        
    def __eq__(self, drob2):
        if (self - drob2).ch==0:
            return True
        else:
            return False
        
    def __ne__(self, drob2):
        if (self - drob2).ch!=0:
            return True
        else:
            return False

##______________________________________
    def __iadd__(self, drob2):
        return self+drob2
    
    def __isub__(self, drob2):
        return self-drob2

    def __imul__(self,drob2):
        return self*drob2
    
    def __itruediv__(self,drob2):
        return self/drob2
    
    def __idiv__(self,drob2):
        return self/drob2

    def __ipow__(self,val):
        return self**val

##__________________________________________________________
    def base_conv(self, base=10):
        if base > 10:
            return 'use base_conv_l'
        
        if self.ch<0:
            c = '-'
        else:
            c=''
            
        num = abs(self.ch) // self.zn
        c += delit(num, base)
        c += '.'

        dr = abs(self.ch) % self.zn
        zn = self.zn
        st_e = step_enter(self.zn, base)
        nd = nod(base, zn // (base ** st_e))

        while nd != 1:
            zn *= base // nd
            dr *= base // nd
            st_e += 1
            nd = nod(base, zn // (base ** st_e))

        for e in range(st_e):
            zn //= base
            c += str(dr // zn)
            dr = dr % zn

        n = 1
        while (base ** n - 1) % zn != 0 and n <= zn:
            n += 1

        dr = dr * (base ** n - 1) // zn
        dr = delit(dr, base)
        c = c + '(' + '0' * (n - len(dr)) + dr + ')'

        return c

    ##
    def base_conv_l(self, base):
        if base <= 10:
            return 'use base_conv'

        if self.ch<0:
            c = '-'
        else:
            c=''
        num = abs(self.ch) // self.zn
        c += delit_l(num, base)
        c += '.'

        dr = abs(self.ch) % self.zn
        zn = self.zn
        st_e = step_enter(self.zn, base)
        nd = nod(base, zn // (base ** st_e))

        while nd != 1:
            zn = zn * (base // nd)
            dr = dr * (base // nd)
            st_e += 1
            nd = nod(base, zn // (base ** st_e))

        for e in range(st_e):
            zn //= base
            n = dr // zn
            if n <= 10:
                c += str(n)
            elif 10 < n <= 36:
                c += chr(n + ord('A') - 10)
            else:
                c += '[' + str(n) + ']'
            dr = dr % zn
        n = 1
        while (base ** n - 1) % zn != 0 and n <= zn:
            n += 1
        dr = dr * (base ** n - 1) // zn
        dr,i = delit_l(dr, base,j=True)
        c = c + '(' + '0' * (n - i) + dr + ')'

        return c







# #############################################################__nod

def nod(ch, zn):
    while zn!=0:
        ch %= zn
        ch,zn = zn,ch
    return ch

# ###########################_____tools
def delit(num, base):
    c = ''
    if num != 0:
        while num >= base:
            c += str(num % base)
            num = num // base
        if num != 0:
            c += str(num)
    else:
        c = '0'
    return c[::-1]


#
def delit_l(num, base,j=False):
    c = ''
    i=0
    if num != 0:
        while num >= 1:
            i+=1
            a = num % base
            num = num // base
            if 10 <= a < 36:
                c = chr(a + ord('A') - 10)+c
            elif a >= 36:
                c = '[' + str(a) + ']'+c
            else:
                c = str(a)+c
        if j:
            return c,i
        else:
            return c
    else:
        c = '0'
    if j:
        return c,i
    else:
        return c


#
def step_enter(num, a):
    c = 0
    while num % a == 0:
        c += 1
        num = num // a
    return c


def to_drob(a):
    n=1
    while a%1!=0:
        n*=10
        a*=10
    return drob(int(a),n)



##############################################################
class jdrob(drob):
    def __init__(self,a=drob(0,1),b=drob(0,1)):
        self.re = a
        self.im = b
        self.mod2 = self.re**2+self.im**2
        self._ = self.re._+'+('+self.im._+')j'
        self.val = complex(self.re.val,self.im.val)


    def drob(self):
        print(self, ' = ', self.re.base_conv(),'+(',
                  self.im.base_conv(),')j', sep='')


    def base_conv(self,base=10):
        return self.re.base_conv(base)+'+('+self.im.base_conv(base)+')j'
    
    def base_conv_l(self,base):
        return self.re.base_conv_l(base)+'+('+self.im.base_conv_l(base)+')j'

        
    def __str__(self):
        return self._
##__________________________________________________________
    def __neg__(self):
        return jdrob(-self.re,-self.im)

    def __pos__(self):
        return self
    
    def __abs__(self):
        return (self.mod2.val)**0.5
    
    def __bool__(self):
        return (self.re!=drob(0,1) or self.im!=drob(0,1))

#______________________________________________________________
    def __add__(self, jdrob2):
        return jdrob(self.re+jdrob2.re,self.im+jdrob2.im)
    
    def __sub__(self, jdrob2):
        return jdrob(self.re-jdrob2.re,self.im-jdrob2.im)

    def __mul__(self,jdrob2):
        return jdrob(self.re*jdrob2.re-self.im*jdrob2.im,
                     self.re*jdrob2.im+self.im*jdrob2.re)
    
    def __truediv__(self,jdrob2):
        return jdrob((self.re*jdrob2.re+self.im*jdrob2.im)/(jdrob2.re**2+jdrob2.im**2),
                     (self.im*jdrob2.re-self.re*jdrob2.im)/(jdrob2.re**2+jdrob2.im**2))
    
    def __div__(self,jdrob2):
        return self.__truediv__(jdrob2)
    
    def __pow__(self,val):
        if not isinstance(val,int):
            return complex(self.re.val,self.im.val)**val
            #raise TypeError('value must be integer')
        if val>=0:
            c = jdrob(drob(1,1),drob(0,1))
            for e in range(val):
                c = c*self
            return c
        else:
            c = jdrob(drob(1,1),drob(0,1))
            for e in range(-val):
                c = c/self
            return c
##___________________________________________________________
    def __eq__(self, jdrob2):
        c = self - jdrob2
        if c.re.ch==0 and c.im.ch==0:
            return True
        else:
            return False
        
    def __ne__(self, jdrob2):
        c = self - jdrob2
        if c.re.ch!=0 or c.im.ch!=0:
            return True
        else:
            return False
##_____________________________________________________________
    def __iadd__(self, jdrob2):
        return self+jdrob2
    
    def __isub__(self, jdrob2):
        return self-jdrob2

    def __imul__(self,jdrob2):
        return self*jdrob2
    
    def __itruediv__(self,jdrob2):
        return self/jdrob2
    
    def __idiv__(self,jdrob2):
        return self/jdrob2
    
    def __ipow__(self,val):
        return self**val
