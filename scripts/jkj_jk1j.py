# Online Python - IDE, Editor, Compiler, Interpreter
if __name__ == "__main__":
        k1 = int(input('Enter Ka1: '))
        j = int(input('Enter J0: '))
        jn = int(input('Enter Jn: '))
        x = ""
        y = "     "
        k2 = k1 + 1
        while j <= jn:
            Ka = k1
            J = j
            Kc = J - Ka 
            print( y,J,x,Ka,x,Kc )
        
def generateMatrix(Ka, J, Kc):
        delta_J = [-1,0,1]
        delta_Ka = [0,2,-2]
        delta_Kc = [-3,-1,1,3]
        result = ""
        for i in range(3):
            d1= delta_Ka[i]
            ka = Ka + d1
            for dJ in range(3):
                d2 = delta_J[dJ]
                j = J + d2
                for dKc in range(4):
                    d3 = delta_Kc[dKc]
                    kc = Kc + d3
                    s = ka + kc
                    sm = j+1
                    if ((j>0)and((ka>=0)and(kc>=0))and((s==j)or(s==sm))and((ka<=j)and(kc<=j)) and ka >= 0 and kc >= 0 and j > 0):
                        line = str(j) + "  " + str(ka) + "  " + str(kc)
                        #print(line)
                        result += line + '\n' 
        return result
        Ka = k2
        J = j
        Kc = J - Ka + 1  
        print( y,J,x,Ka,x,Kc )
        
        delta_J = [-1,0,1]
        delta_Ka = [0,2,-2]
        delta_Kc = [-3,-1,1,3]
        for i in range(3):
            d4= delta_Ka[i]
            ka = Ka + d4
            for dJ in range(3):
                d5 = delta_J[dJ]
                j = J + d5
                for dKc in range(4):
                    d6 = delta_Kc[dKc]
                    kc = Kc + d6
                    s = ka + kc
                    sm = j+1
                    if ((j>0)and((ka>=0)and(kc>=0))and((s==j)or(s==sm))and((ka<=j)and(kc<=j))):
                        print( j, x, ka, x, kc )

        j = j + 1
        print()
