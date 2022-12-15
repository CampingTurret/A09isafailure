
from codeinertia import t_spar as t1, t as t2, spanInternalShear as SIS, V1 as V1, sigma_y1 as sigmax, n as numstring, sigma_max1 as maxsig, tau_max1 as maxtau, v1 ,theta1 , front_spar as fs
import numpy as np
from math import pi
from skinbuckling import skinsearch
import matplotlib.pyplot as plt
import os
import sys
import subprocess

w = float(input("Stringer thickness [m]: "))


def ribsearch():
    y = np.linspace(0,10.1,400)
    ribplacement = np.full(400, False )
    ribplacement[0] = True
    index = 0
    while(True):
        if(index>=399):
            ribplacement[399] = True
            return ribplacement
        x1 = websearch(index)
        x2 = skinsearch(index, sigmax)
        #x3 = columnsearch(index,sigmax)

        xpos = min(x1,x2)
        print(xpos)
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
        yindex = yindex +1
        if(yindex > 399):
            return 399
        continu = check(yindex, ystart,t,y)
        

  
    yend = yindex - 1
    
    return yend

def check(ye,yb,t,y):
    a = y[ye] - y[yb]
    c = 3.44 - (2* 3.44 *(0.6))/(20.2) * y[yb]    
    hf= c * 0.1121629
    hb = c * 0.058208
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
                print("front")
                return False

    if(abrb>1):
        ksb = 4.982/(abrb**2.311) +9.378
        #ksb = 0.1773*abrb**4 - 2.4181*abrb**3 + 12.044*abrb**2 - 26.253*abrb + 31.115
        if (abrb>5):
            ksb = 9.5
        for x in range(np.size(y[yb:ye])):

            taucr = taucrit(ksb,t,hb)
            taumax = taub[yb+x]

            if(taumax>taucr):
                print("back")
                return False

    return True

#-----------------------

def sigmacrit(k_c, b, t):

    # h1, h2, w1, w2, A = airfoilparameters(0.2, 0.75)
    E = 68.9 * 10**9
    v = 1/3
    sigma = (pi**2*k_c*E*(t**2))/(12*(1-v**2)*(b**2))

    return sigma


def check2(ye, yb, t, y, stress):
    a = y[ye] - y[yb]
    b = 0.55*(3.44 - (2 * 3.44 * (0.6)) / (20.2) * y[yb])/(numstring+1)

    ksc = 3.178*(b**2.082)/(a**2.082)+7.173
    #ksc = 7
    #ksc = 4
    if(a/b > 5): ksc = 7.2
    for x in range(np.size(y[yb:ye])):

        sigmacr = sigmacrit(ksc, b, t)
        sigmamax = stress[yb + x]

        if (sigmamax > sigmacr):
            print(sigmacr)
            print(sigmamax)
            print(ksc)
            return False

    return True


def skinsearch(ystart, stress):
    yindex = ystart
    t = t2

    y = np.linspace(0.0, 10.1, 400)
    continu = True

    while (continu):
        yindex = yindex + 1
        if (yindex > 399):
            return 399
        continu = check2(yindex, ystart, t, y, stress)

    yend = yindex - 1

    return yend

#-----------------------

def columnsearch(ystart, stress):
    yindex = ystart
    

    y = np.linspace(0.0, 10.1, 400)
    continu = True

    while (continu):
        yindex = yindex + 1
        if (yindex > 399):
            return 399
        continu = check3(yindex, ystart, w, y, stress)

    yend = yindex - 1

    return yend

def check3(ye, yb, t, y, stress):
    a = y[ye] - y[yb]
    b = 0.55*(3.44 - (2 * 3.44 * (0.6)) / (20.2) * y[yb])/(numstring+1)

    ksc = 3.178*(b**2.082)/(a**2.082)+7.173
    #ksc = 7
    #ksc = 4
    if(a/b > 5): ksc = 7.2
    for x in range(np.size(y[yb:ye])):

        sigmacr = sigmacrit(ksc, b, t)
        sigmamax = stress[yb + x]

        if (sigmamax > sigmacr):
            print(sigmacr)
            print(sigmamax)
            print(ksc)
            return False

    return True

#-----------------------
print("------------------------------------------------")
tauf, taub = SIS(V1,t1,0)
x = ribsearch()
print("------------------------------------------------")
if (max(abs(maxtau),abs(fs))<207):
    print("structure survives shear")
else : print("structure fails shear")
if (abs(maxsig)< 276) :
    print("structure survives bending")
else: print("structure fails bending")
if (abs(np.sum(theta1)) < 0.174):
    print("structure survives twist")
else: print("structure fails twist")
if (abs(np.sum(v1)) < 3.03):
    print("structure survives deflection")
else: print("structure fails deflection")
print("------------------------------------------------")

print("number or ribs:" + str(np.sum(x)))

y = np.linspace(0,10.1,400)
plt.bar(y,x,width = 0.08)
plt.show()
print("-------------------------------------------------------------")
print("Restarting")
print("-------------------------------------------------------------")
print("Warning watch out for memory leaks")
print("-------------------------------------------------------------")
subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
