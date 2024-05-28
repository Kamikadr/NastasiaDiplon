# Online Python - IDE, Editor, Compiler, Interpreter


k1 = int(input('Enter Ka1: '))
b = int(input('Enter J0: '))
d = int(input('Enter Jn: '))
x = ""
y = "     "
k2 = k1 + 1
while b <= d:
    Ka = k1
    J = b
    Kc = J - Ka 
    print( y,J,x,Ka,x,Kc )
    
    delta_J = [-1,0,1]
    delta_Ka = [0,2,-2]
    delta_Kc = [-3,-1,1,3]
    for dKa in range(3):
        d1= delta_Ka[dKa]
        ka = Ka + d1
        for dJ in range(3):
            d2 = delta_J[dJ]
            j = J + d2
            for dKc in range(4):
                d3 = delta_Kc[dKc]
                kc = Kc + d3
                s = ka + kc
                sm = j+1
                if ((j>0)and((ka>=0)and(kc>=0))and((s==j)or(s==sm))and((ka<=j)and(kc<=j))):
                    print( j, x, ka, x, kc )

    b = b + 1
    print()
