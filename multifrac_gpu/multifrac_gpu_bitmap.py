from numba import jit, complex128, int64, float64, prange
from multifrac_gpu_H import H
##from multifrac_gpu_D import D

@jit(complex128[:](complex128[:],complex128,int64),nopython=True, nogil=True, parallel=True)
def bitmap(pic,c,deph):
    for i in prange(len(pic)):
        pic[i] = H(pic[i],c,deph)
    return pic


##@jit(float64[:,:](complex128[:],complex128,int64,int64),nopython=True, nogil=True, parallel=True)
##def ani_bitmap(pic,c,deph,frames):
##    ims = np.array([[]*frames])
##    for i in range(frames):
##        print(i)
##        ims[i] = f_bitmap.bitmap(pic,c,deph).real
##        c = D(c)
##    return ims
