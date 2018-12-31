def new_F(s):
    f_file = open("multifrac_gpu_F.py","w")
    f_file.write('''from numba import jit, complex128
import numpy as np

@jit(complex128(complex128,complex128),nopython=True)
def F(z,c):
    return %s ''' % (s))
    f_file.close()
    
    return None

def new_G(s):
    g_file = open("multifrac_gpu_G.py","w")
    g_file.write('''from numba import jit, complex128, int64, float64
import numpy as np

@jit(float64(complex128,int64,int64),nopython=True)
def G(z,k,deph):
    return %s''' % (s))
    g_file.close()
    
    return None

def new_H(s):
    h_file = open("multifrac_gpu_H.py","w")
    h_file.write('''from numba import jit, complex128,float64,int64
from multifrac_gpu_F import F
from multifrac_gpu_G import G

@jit(float64(complex128,complex128,int64),nopython=True)
def H(z,c,deph):
    %s
    return G(z,k,deph)''' % (s))
    h_file.close()
    
    return None
