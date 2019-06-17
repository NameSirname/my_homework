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


def length(v):
    return np.sqrt(v[0]*v[0]+v[1]*v[1])

def rotate(v,rot):
    return np.array([sum(v*rot[0]),sum(v*rot[1])])   

def get_vec(angles,vec,i):
    if 90<angles[i]<270:
        vec[i] = np.array([-1,-np.tan(angles[i]/180*np.pi)])
    elif angles[i] == 90:
        vec[i] = np.array([0,1])
    elif angles[i] == 270:
        vec[i] = np.array([0,-1])
    else:
        vec[i] = np.array([1,np.tan(angles[i]/180*np.pi)])
    vec[i] /= length(vec[i]) 
    return None

#returns bisector vector vec of angle between v1 and v2 -- vectors of length 1,
#ai is angle between vi and basic vector v (P2-P1)
def vecL(v1,v2,a1,a2):
    vec = v1+v2
    l = length(vec)
    if l>0 : vec = vec/l
    if a2-a1 > 180 or 0>a2-a1>-180: vec*=-1
    if abs(a2-a1) == 180:
        vec[0],vec[1] = -v1[1],v1[0]
    return vec

#vec is offset vector, v is vector collinear to the border, P is start point
def borderL(P,vec,v,con_num,w1,w2):
    Q = P+vec
    for k in range(con_num):
            ax.plot([Q[0],Q[0]+v[0]*2],[Q[1],Q[1]+v[1]*2],
                    linewidth = (w1+w2)/2,color = 'black')
            Q += vec
##            if connections[i]>1: Q += vec1/(connections[i]-1)
    return None   

def draw_lines(n,vec,P,angles,connections,widths,nums,eps):
    global ax
    for i in range(n):
        vec1 = vecL(vec[i],vec[i+1],angles[i],angles[i+1])*eps
        vec2 = vecL(vec[i-1],vec[i],angles[i-1],angles[i])*eps
        
        if abs(sum(vec[i]*vec1))>abs(sum(vec[i]*vec2)):
            Q = P+vec1
            vec3 = np.array([vec[i][1],-vec[i][0]])
        else:
            Q = P+vec2
            vec3 = np.array([-vec[i][1],vec[i][0]])
            
        l = abs(sum((vec1-vec2)*vec3))
        vec3*=l
        for k in range(nums[i]):
            Q += vec3/(nums[i]+1)
            ax.plot([Q[0],Q[0]+vec[i][0]*2],[Q[1],Q[1]+vec[i][1]*2],
                    linewidth = widths[i],color = 'black')

        if i!=n-1: borderL(P,vec1,vec[i],connections[i],widths[i],widths[i+1])
        if i!=0: borderL(P,vec2,vec[i],connections[i-1],widths[i],widths[i-1])
            
    return None

#v is vector of length 1, collinear to P2-P1, vec1 and vec2 are border vectors,
#aij - corresponding angles
def bridge(P1,P2,i,v,vec1,a11,a12,vec2,a21,a22,con1,w11,w12,con2,w21,w22,eps):
    if i:
        v1 = vecL(v, vec1, a11, a12)
        v2 = vecL(vec2,-v, a21, a22)
    else:
        v1 = vecL(vec1, v, a11, a12)
        v2 = vecL(-v, vec2, a21, a22)

    s1 = abs(v1[0]*v[1]-v1[1]*v[0]) #calculate sin
    s2 = abs(v2[0]*v[1]-v2[1]*v[0])
    if s1>s2:
        v2*=s1/s2
    else:
        v1*=s2/s1
    v1*=eps
    v2*=eps
    borderL(P1,v1,vec1,min(con1,con2),w11,w12)
    borderL(P2,v2,vec2,min(con1,con2),w21,w22)

    for i in range(1,min(con1,con2)+1):
        ax.plot([P1[0]+v1[0]*i,P2[0]+v2[0]*i],[P1[1]+v1[1]*i,P2[1]+v2[1]*i],
                linewidth = w22,color = 'black')

    if con1 < con2:
        borderL(P2+v2*con1,-v*abs(sum(v*v2)),vec2,con2-con1,w21,w22)
    else:
        borderL(P1+v1*con2,v*abs(sum(v*v1)),vec1,con1-con2,w11,w12)
    

    return v1,v2


##______________________

def gen(angles1, angles2, num=0, nums1=[], nums2=[],#array of angles between lines in degrees
         connections1=[], connections2=[], widths1=[], widths2=[], eps=0.025): 
    global ax
    n1 = len(angles1)
    n2 = len(angles2)
    if len(widths1)<n1+1: widths1 += [1]*(n1+1-len(widths1))
    if len(nums1)<n1: nums1 += [0]*(n1-len(nums1))
    if len(connections1)<n1+1: connections1 += [1]*(n1+1-len(connections1))
    
    if len(widths2)<n2+1: widths2 += [1]*(n2+1-len(widths2))
    if len(nums2)<n2: nums2 += [0]*(n2-len(nums2))
    if len(connections2)<n2+1: connections2 += [1]*(n2+1-len(connections2))
    
    set_ax()
##    P1 = rnd.random([2])
##    P2 = rnd.random([2])
    P1 = np.array([0.25,0.25])
    P2 = np.array([0.75,0.75])
    v = P2-P1
    rot = np.array([[v[0],-v[1]],
                       [v[1],v[0]]])/length(v)
    vec1 = np.empty([n1+1,2])
    vec2 = np.empty([n2+1,2])

    angles1[0] = angles1[0]%360 #%90
    get_vec(angles1,vec1,0)
    vec1[0] = rotate(vec1[0],rot)
    angles2[0] = angles2[0]%360 #%90
    get_vec(angles2,vec2,0)
    vec2[0] = -rotate(vec2[0],rot)
    for i in range(1,n1):
        angles1[i] = (angles1[i]+angles1[i-1])%360
        get_vec(angles1,vec1,i)
        vec1[i] = rotate(vec1[i],rot)
    for i in range(1,n2):
        angles2[i] = (angles2[i]+angles2[i-1])%360
        get_vec(angles2,vec2,i)
        vec2[i] = -rotate(vec2[i],rot)

    v/=length(v)
    vec1[n1] = v
    vec2[n2] = -v
    angles1.append(0)
    angles2.append(0)

    draw_lines(n1,vec1,P1,angles1,connections1,widths1,nums1,eps)
    draw_lines(n2,vec2,P2,angles2,connections2,widths2,nums2,eps)
    

    v1,v2 = bridge(P1,P2,1,v,vec1[0],0,angles1[0],vec2[n2-1],angles2[n2-1],0,
           connections1[n1],widths1[0],widths1[n1],
           connections2[n2-1],widths2[n2-1],widths2[n2],eps)
    v3,v4 = bridge(P1,P2,0,v,vec1[n1-1],angles1[n1-1],0,vec2[0],0,angles2[0],
           connections1[n1-1],widths1[n1-1],widths1[n1],
           connections2[n2],widths2[0],widths2[n2],eps)

    Q1,Q2 = P1+v1,P2+v2
    for k in range(num):
            Q1 += (v3-v1)/(num+1)
            Q2 += (v4-v2)/(num+1)
            ax.plot([Q1[0],Q2[0]],[Q1[1],Q2[1]],
                    linewidth = widths1[-1],color = 'black')


    plt.show(block = False)
    plt.savefig("filename.svg", bbox_inches = 'tight',pad_inches = 0)
    return None

##____________________

def rand_angles(n=1,a1=30,a2=30):
    angles = [a1]

    s = angles[0]
    less = 10
    for i in range(1,n):
        angles.append(rnd.randint(less,min(90,180+a2-s-less*(n-1-i))))
        s += angles[i]
    return angles

fig,ax = plt.subplots(1)
fig.tight_layout(pad=0,rect=[0,0,1,1])
fig.set_size_inches(4,4)


##gen([60,90],[45,45,90],[1,2],[0,3,1],[],[1,2])

##a2 = rand_angles(4)
##a1 = rand_angles(4)
##gen(a1,a2,1,[0,0,1,1],[1,0,1,0],[3,2,1,0],[0,2,0,3])
