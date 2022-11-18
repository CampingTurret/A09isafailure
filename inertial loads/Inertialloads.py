import math


def fuelvolume(A,Cr,b,labda):
    V = A*Cr*Cr*b*(labda*labda + labda + 1)/3
    return V


def wingvolume(A,Cr,b,labda):
    V = A*Cr*Cr*b*(labda*labda + labda + 1)/3
    return V

def fuelloading(p,g,A,Cr,b,labda,y):
    w = p * g * A * Cr * Cr *()
    return w