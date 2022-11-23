import math
import scipy as sc
import scipy.integrate as integrate
import numpy as np
import pandas


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
    c2 = b * b *(ratio*ratio/48 - ratio/12 + 1/8 -(labda*labda+labda+1)/12)
    V = p * g * A * Cr * Cr *(-4/(12*b*b)*ratio * ratio * y * y * y*y +2/(3*b) * ratio * y * y *y - 0.5* y*y + c1*y + c2)
    return V


def fueltorque():



    return T



def structureArea(y, array, Cr, b, labda):
    a = array

    for q in range(a.ndim):
        bound1 = a[0,q]
        bound2 = a[1,q]

        




        if bound1 < y:
            if bound2 >= y:

                t = a[2,q]

                c = Cr - Cr * (1-labda) * 2* y / b


                h1 = c * 0.108861
                h2 = c * 0.128807
                w1 = c * 0.550489
                w2 = c * 0.550010
                circumference = h1 + h2 + w1 + w2
                area = t * circumference
                
                W = area
                return W


    return 0



def structureloading(y, array, p, g, Cr, b, labda ):
    a = array
    for q in range(a.shape[1]):
        bound1 = a[q,0]
        bound2 = a[q,1]
        if bound1 < y:
            if bound2 >= y:

                t = a[q,2]

                c = Cr - Cr * (1-labda) * 2* y / b


                h1 = c * 0.108861
                h2 = c * 0.128807
                w1 = c * 0.550489
                w2 = c * 0.550010
                circumference = h1 + h2 + w1 + w2
                area = t * circumference
                
                W = area * p * g
                return W

    print("ERROR OUT OF BOUNDS")
    return 0


def structuredensity(m1,m2,b,array,Cr,labda):


    M = m1 - m2

    V = integrate.quad(structureArea,0,b/2, args=(array,Cr,b,labda))

    q = M/(V[0])
    return q

def wingletweight(m1,V1,V2):


    q = m1/(V1+V2)
    m2 = q *V2

    return m2


def structureshear(y, array, p, g, Cr, b, labda, m2):
    
    V = -integrate.quad(structureloading,0,y, args=(array,p,g,Cr,b,labda))[0] - integrate.quad(structureloading,0,b/2, args=(array,p,g,Cr,b,labda))[0] + m2 *g

    return V

def structureMoment(y, array, p, g, Cr, b, labda ,m2):

    M = integrate.quad(structureshear,0,y, args=(array,p,g,Cr,b,labda, m2))[0] - integrate.quad(structureshear,0,b/2, args=(array,p,g,Cr,b,labda, m2))[0]

    return M

