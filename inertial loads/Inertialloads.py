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
    ratio = 1 - labda
    c1 = b/6 *(labda * labda + labda + 1)
    c2 = b * b *(ratio*ratio/24 - ratio/12 + 1/8 -(labda*labda+labda+1)/12)
    V = p * g * A * Cr * Cr *(4/(12*b*b)*ratio * ratio * y * y * y*y +2/(3*b) * ratio * y * y *y + 0.5* y*y - c1*y + c2)
    return V


def fueltorque():



    return T

def structureloading(array, p, g, Cr, b ,y):

    for in array


    return W





