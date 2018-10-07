def simple_nums(zn):
    A=[1 for i in range(2,zn)]
    for e in range(int(len(A)**(1/2))):
        if A[e]:
            for i in range(e,len(A),e+2):
                A[i]=0
            A[e]=1
    for e in range(len(A)):
        if A[e]:
            print(e+2, end=' ')
    return None
            
