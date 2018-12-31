from numba import jit, complex128
import numpy as np

@jit(complex128(complex128,complex128),nopython=True)
def F(z,c):
    return z*z+c 