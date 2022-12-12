
from re import A
from codeinertia import t_spar as t1, spanInternalShear as SIS, V1 as V1
from main import sum_shear1
import numpy as np
from math import pi
#from skinbuckling import as skinsearch





#def shearflowtorsion(t,c,T):

#    h1,h2,w1,w1,a = afp(0.2,0.75)

#    tau = T/(2*a*c*t)


#    return tau


#def shearV(t,c,V):
#    kv = 1.2
#    h1,h2,w1,w1,a = afp(0.2,0.75)
#
#   tau = V/((h1+h2)*t*c)
#    tau = tau * kv
#
#    return tau

def ribsearch():
    y = np.linspace(0,10,1,400)
    ribplacement = np.full(400, False )
    ribplacement[0] = True
    index = 0
    while(True):
        if(index>=399):
            ribplacement[399] = True
            return ribplacement
        x1 = websearch(index)
        #x2 = skinsearch(index)

        xpos = x1 #min(x1,x2)

        if(xpos>399):
            ribplacement[399] = True
            return ribplacement
            

        ribplacement[xpos] = True

        index = xpos
        

    






def taucrit(ks,t,b):

    E = 68.9 * 10**9
    v = 1/3
    taucr = (pi*pi*ks*E*t*t)/(12*(1-v*v)*b*b)
    return taucr


def websearch(ystart):
    yindex = ystart
    t = t1

    y = np.linspace(0.0, 10.1, 400)
    continu = True
    
    while(continu):

        continu = check(yindex, ystart,t,y)
        print(yindex)
        yindex = yindex +1

        if(yindex > 399):
            return 399

    

    yend = yindex - 1
    
    return yend


def check(ye,yb,t,y):


    a = y[ye] - y[yb]
    print(a)

    c = 3.44 - (2* 3.44 *(0.6))/(20.2) * y[yb]    
    hf= c * 0.128807
    hb = c * 0.108861
    abrf = a/hf
    abrb = a/hb
    
    if(abrf>1):
        #ksf = 0.1773*abrf**4 - 2.4181*abrf**3 + 12.044*abrf**2 - 26.253*abrf + 31.115

        ksf = 4.982/(abrf**2.311) +9.378

        if (abrf>5):
            ksf = 9.5
        
        for x in range(np.size(y[yb:ye])):
 
            taucr = taucrit(ksf,t,hf)
            taumax = tauf[yb+x]

            if(taumax>taucr):
                return False


    if(abrb>1):
        ksb = 4.982/(abrb**2.311) +9.378
        #ksb = 0.1773*abrb**4 - 2.4181*abrb**3 + 12.044*abrb**2 - 26.253*abrb + 31.115
        if (abrb>5):
            ksf = 9.5
        for x in range(np.size(y[yb:ye])):

            taucr = taucrit(ksb,t,hb)
            taumax = taub[yb+x]

            if(taumax>taucr):
                return False

    return True

print("------------------------------------------------")
tauf, taub = SIS(V1,t1,0)
x = ribsearch()
print("rib pos")
print(x)

print(np.sum(x))
