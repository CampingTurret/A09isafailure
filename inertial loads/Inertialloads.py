import math
import scipy
import numpy


def fuelvolume(A,Cr,b,labda):
    V = A*Cr*Cr*b*(labda*labda + labda + 1)/3
    return V


def wingvolume(A,Cr,b,labda):
    V = A*Cr*Cr*b*(labda*labda + labda + 1)/3
    return V

def fuelloading(p,g,A,Cr,b,labda,y):

    ratio = 1 - labda
    w = p * g * A * Cr * Cr *(4/(b*b)*ratio * ratio * y * y -4/b * ratio * y  + 1)
    return w

def fuelshear(p,g,A,Cr,b,labda,y): 
    c1 = b/6 *(labda * labda + labda + 1)
    ratio = 1 - labda
    V = p * g * A * Cr * Cr *(-4/(3*b*b)*ratio * ratio * y * y * y +2/b * ratio * y * y - y + c1)
    return 


def fuelmomenent(p,g,A,Cr,b,labda,y): 
    c1 = b/6 *(labda * labda + labda + 1)
    c2 = 
    ratio = 1 - labda
    V = p * g * A * Cr * Cr *(-4/(3*b*b)*ratio * ratio * y * y * y +2/b * ratio * y * y - y + c1)
    return V


def fueltorque():



    return T

def structureloading(array, p, g, Cr, b ,y):


    return W
