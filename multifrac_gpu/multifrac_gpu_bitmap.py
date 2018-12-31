from numba import jit, complex128, int64, float64, prange
from multifrac_gpu_H import H

@jit(complex128[:](complex128[:],complex128,int64),nopython=True, nogil=True, parallel=True)
def bitmap(A,c,deph):
    for i in prange(len(A)):
        A[i] = H(A[i],c,deph)
    return A
