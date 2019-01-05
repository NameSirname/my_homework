from numba import jit, complex128, int64, float64
import numpy as np

@jit(float64(complex128,int64,int64),nopython=True)
def G(z,k,deph):
    return k+np.angle(z)*deph/10/(k+2)