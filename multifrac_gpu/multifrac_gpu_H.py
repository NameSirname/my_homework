from numba import jit, complex128,float64,int64
from multifrac_gpu_F import F
from multifrac_gpu_G import G

@jit(float64(complex128,complex128,int64),nopython=True)
def H(z,c,deph):
    for k in range(deph):
        z = F(z,c)
        c = z+c/2
        if (abs(z)>5):
            break
    return G(z,k,deph)