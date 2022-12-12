
from codeinertia import airfoilparameters as afp
import numpy as np
from math import pi




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

def sparsearch(desarray1,desarray2,desarray3,tau,sigma):
    y = np.linspace(0,10,1,400)
    sparplacement = np.empty(400, bool)
    



    return sparplacement





def taucrit(ks,t,b):

    E = 68.9 * 10**9
    v = 1/3

    taucr = (pi*pi*ks*E*t*t)/(12*(1-v*v)*b*b)


    return taucr


def webspar(ystart,t):
    yindex = ystart

    y = np.linspace(0.0, 10.1, 400)

    
    while(check(yindex, ystart,t,y)):

        yindex = yindex +1

    

    yend = yindex - 1

    

    
    return yend


def check(ye,yb,t,y):


    a = y[ye] - y[yb]

    c = 3.44 - (2* 3.44 *(0.6))/(20.2) * y[ye]    
    hf= c * 0.128807
    hb = c * 0.108861
    abrf = a/hf
    abrb = a/hb
    
    if(abrf>1):
        ksf = 0.1773*abrf**4 - 2.4181*abrf**3 + 12.044*abrf**2 - 26.253*abrf + 31.115

        if (abrf>5):
            ksf = 9.5
        
        for x in range(np.size(y[yb:ye])):
            taucr = taucrit(ksf,t,hf)
            taumax = [yb+x]

            if(taumax>taucr):
                return False


    if(abrb>1):
        ksb = 0.1773*abrb**4 - 2.4181*abrb**3 + 12.044*abrb**2 - 26.253*abrb + 31.115
        if (abrb>5):
            ksf = 9.5
        for x in range(np.size(y[yb:ye])):
            taucr = taucrit(ksb,t,hb)
            taumax = [yb+x]

            if(taumax>taucr):
                return False





    return True



