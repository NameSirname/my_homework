import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from numpy import random as rnd

def set_ax():
    ax.clear()
    ax.axis('scaled')
    ax.axis([0,1,0,1])
    ax.axis('off')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    return None

def gen(angles, nums=[],widths=[],eps=0.025): #array of angles in degrees
    global ax
    n = len(angles)
    if len(widths)<n: widths += [1]*(n-len(widths))
    if len(nums)<n: nums += [1]*(n-len(nums))
    
    set_ax()
    P = rnd.random([2])
    vec = np.empty([n,2])
    for i in range(n):
        angles[i] = angles[i]%360
        if 90<angles[i]<270:
            vec[i] = np.array([-1,-np.tan(angles[i]/180*np.pi)])
        elif angles[i] == 90:
            vec[i] = np.array([0,1])
        elif angles[i] == 270:
            vec[i] = np.array([0,-1])
        else:
            vec[i] = np.array([1,np.tan(angles[i]/180*np.pi)])
        vec[i]/=np.sqrt(vec[i][0]*vec[i][0]+vec[i][1]*vec[i][1])

    for i in range(n):
        vec1 = vec[i]+vec[(i+1)%n]
        l = np.sqrt(vec1[0]*vec1[0]+vec1[1]*vec1[1])
        if l>0 : vec1 = vec1*eps/l
        if (angles[(i+1)%n]-angles[i] > 180 or
            0>angles[(i+1)%n]-angles[i]>-180): vec1*=-1
        if abs(angles[i]-angles[(i+1)%n]) == 180:
            vec1[0],vec1[1] = -eps*vec[i][1],eps*vec[i][0]
            
        vec2 = vec[i]+vec[(i-1)%n]
        l = np.sqrt(vec2[0]*vec2[0]+vec2[1]*vec2[1])
        if l>0 : vec2 = vec2*eps/l
        if (angles[i]-angles[(i-1)%n]>180 or
            0>angles[i]-angles[(i-1)%n]>-180): vec2*=-1
        if abs(angles[i]-angles[(i-1)%n]) == 180:
            vec2[0],vec2[1] = eps*vec[i][1],-eps*vec[i][0]

        vec2 -= vec1

        Q = P+vec1
        for k in range(nums[i]+1):
            ax.plot([Q[0],Q[0]+vec[i][0]*2],[Q[1],Q[1]+vec[i][1]*2],
                    linewidth = widths[i],color = 'black')
            Q += vec2/nums[i]
            
    plt.show(block = False)
    plt.savefig("filename.svg", bbox_inches = 'tight',pad_inches = 0)
    return P



##_____________________________________________________



def gen1(angles, nums=[],connections=[],
         widths=[],eps=0.025): #array of angles in degrees
    global ax
    n = len(angles)
    if len(widths)<n: widths += [1]*(n-len(widths))
    if len(nums)<n: nums += [1]*(n-len(nums))
    if len(connections)<n: connections += [1]*(n-len(connections))
    
    set_ax()
    P = rnd.random([2])
    vec = np.empty([n,2])
    for i in range(n):
        angles[i] = angles[i]%360
        if 90<angles[i]<270:
            vec[i] = np.array([-1,-np.tan(angles[i]/180*np.pi)])
        elif angles[i] == 90:
            vec[i] = np.array([0,1])
        elif angles[i] == 270:
            vec[i] = np.array([0,-1])
        else:
            vec[i] = np.array([1,np.tan(angles[i]/180*np.pi)])
        vec[i]/=np.sqrt(vec[i][0]*vec[i][0]+vec[i][1]*vec[i][1])


    for i in range(n):
        vec1 = vec[i]+vec[(i+1)%n]
        l = np.sqrt(vec1[0]*vec1[0]+vec1[1]*vec1[1])
        if l>0 : vec1 = vec1*eps/l
        if (angles[(i+1)%n]-angles[i] > 180 or
            0>angles[(i+1)%n]-angles[i]>-180): vec1*=-1
        if abs(angles[i]-angles[(i+1)%n]) == 180:
            vec1[0],vec1[1] = -eps*vec[i][1],eps*vec[i][0]
            
        vec2 = vec[i]+vec[(i-1)%n]
        l = np.sqrt(vec2[0]*vec2[0]+vec2[1]*vec2[1])
        if l>0 : vec2 = vec2*eps/l
        if (angles[i]-angles[(i-1)%n]>180 or
            0>angles[i]-angles[(i-1)%n]>-180): vec2*=-1
        if abs(angles[i]-angles[(i-1)%n]) == 180:
            vec2[0],vec2[1] = eps*vec[i][1],-eps*vec[i][0]

        
        m = nums[i]-connections[i]-connections[(i-1)%n]
        if sum(vec[i]*vec1)>sum(vec[i]*vec2):
            Q = P+vec1
            vec3 = np.array([vec[i][1],-vec[i][0]])
        else:
            Q = P+vec2
            vec3 = np.array([-vec[i][1],vec[i][0]])
            
        l = abs(sum((vec1-vec2)*vec3))
        for k in range(m):
            Q += vec3/(m+1)*l
            ax.plot([Q[0],Q[0]+vec[i][0]*2],[Q[1],Q[1]+vec[i][1]*2],
                    linewidth = widths[i],color = 'black')

        Q = P+vec1
        for k in range(connections[i]):
            ax.plot([Q[0],Q[0]+vec[i][0]*2],[Q[1],Q[1]+vec[i][1]*2],
                    linewidth = (widths[i]+widths[(i+1)%n])/2,color = 'black')
            Q += vec1
##            if connections[i]>1: Q += vec1/(connections[i]-1)
            
        Q = P+vec2
        for k in range(connections[(i-1)%n]):
            ax.plot([Q[0],Q[0]+vec[i][0]*2],[Q[1],Q[1]+vec[i][1]*2],
                    linewidth = (widths[i]+widths[(i-1)%n])/2,color = 'black')
            Q+=vec2
##            if connections[(i-1)%n]>1: Q += vec2/(connections[(i-1)%n]-1)


    plt.show(block = False)
    plt.savefig("filename.svg", bbox_inches = 'tight',pad_inches = 0)
    return P




fig,ax = plt.subplots(1)
fig.tight_layout(pad=0,rect=[0,0,1,1])
fig.set_size_inches(4,4)

##def gen1(n,angles=[], widths=[]): #array of angles in degrees
##    global ax
##    if len(angles)<n: widths += [0]*(n-len(angles))
##    if len(widths)<n: widths += [1]*(n-len(widths))
##    set_ax()
##    x,y = rnd.random([2])
##    for i in range(n):
##        angle = angles[i]%360
##        if 90<angle<270:
##            vec = np.array([-1,-np.tan(angle/180*np.pi)])
##        elif angle == 90:
##            vec = np.array([0,1])
##        elif angle == 270:
##            vec = np.array([0,-1])
##        else:
##            vec = np.array([1,np.tan(angle/180*np.pi)])
##        l = np.sqrt(vec[0]*vec[0]+vec[1]*vec[1])
##        vec/=(l/2)
##        ax.plot([x,x+vec[0]],[y,y+vec[1]],linewidth = widths[i],color = 'black')
##    plt.show(block = False)
##    return x,y
