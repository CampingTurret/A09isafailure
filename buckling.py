from codeinertia import airfoilparameters as afp
import numpy as np
from math import pi




def shearflowtorsion(t,c,T):

    h1,h2,w1,w1,a = afp(0.2,0.75)

    tau = T/(2*a*c*t)


    return tau


def shearV(t,c,V):
    kv = 1.2
    h1,h2,w1,w1,a = afp(0.2,0.75)

    tau = V/((h1+h2)*t*c)
    tau = tau * kv

    return tau


def taucrit(ks,E,v,t,c):

    h1,h2,w1,w1,a = afp(0.2,0.75)
   

    taucr1 = (pi*pi*ks*E*t*t)/(12*(1-v*v)*h1*h1*c*c)
    taucr1 = (pi*pi*ks*E*t*t)/(12*(1-v*v)*h2*h2*c*c)


    return






