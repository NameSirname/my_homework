n,m=map(int,input().split())
x1,y1,x2,y2=map(int,input().split())
A=[[1]*(m+2)]+[[1]+list(map(int,input().split()))+[1] for e in range(n)]+[[1]*(m+2)]


def labirint(x1,y1,a):
    global A
    if A[y1+1][x1]==0 or a+1<A[y1+1][x1]:
        A[y1+1][x1]=a+1
        labirint(x1,y1+1,a+1)
    if A[y1-1][x1]==0 or a+1<A[y1-1][x1]:
        A[y1-1][x1]=a+1
        labirint(x1,y1-1,a+1)
    if A[y1][x1+1]==0 or a+1<A[y1][x1+1]:
        A[y1][x1+1]=a+1
        labirint(x1+1,y1,a+1)
    if A[y1][x1-1]==0 or a+1<A[y1][x1-1]:
        A[y1][x1-1]=a+1
        labirint(x1-1,y1,a+1)



if not A[y2][x2]:
    labirint(x1,y1,2)

if A[y2][x2]==0:
    print(-1)
else:
    print(A[y2][x2]-2)

        
        
