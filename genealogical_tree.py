##genealogical tree

n = int(input())
D={}
for e in range(n):
    D[e+1]=list(map(int,input().split()))
                
for j in range(n):
    for e in D.keys():
        p=1
        for i in D.values():
            if e in i:
                p=0
        if p:
            print(e, end=' ')
            del D[e]
            break
        
