
from cmath import sqrt
from codeinertia import t_spar as t1, t as t2, spanInternalShear as SIS, V1 as V1, sigma_y1 as sigmax, n as numstring, sigma_max1 as maxsig, tau_max1 as maxtau, v1 ,theta1 , front_spar as fs, A_stringer as Astring, enc_area as Aenc, volume as Vinc;
import numpy as np
from math import pi
from skinbuckling import skinsearch
from margin_of_safety import plot_margin_of_safety
import matplotlib.pyplot as plt
import os
import sys
import subprocess

ue = np.empty(0)
u = np.append(ue,0)

marf = np.append(ue,0)
marb = np.append(ue,0)
marc = np.append(ue,0)
mars = np.append(ue,0)




w = float(input("Stringer width [m]: "))
tr = float(input("Rib thickness [m]: "))
ts = w - sqrt(w**2 - Astring)
Is = ts*w*w*w/3 + ts**3 *w /3 - ts**4/3

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
        x3 = columnsearch(index,sigmax)

        xpos = min(x1,x2,x3)
        #if (x1 < x2 and x1 < x3): print('web')
        #elif (x2 < x3 and x2 < x1): print('skin')
        #elif (x3 < x1 and x3 <x2): print('column') 
        #print(xpos)
        global u 
        u = np.append(u,xpos)
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

        ksf = 3.948/(abrf**2.452) +5.633

        if (abrf>5):
            ksf = 5.6
        
        for x in range(np.size(y[yb:ye])):
 
            taucr = taucrit(ksf,t,hf)
            taumax = tauf[yb+x]
            
            if(abs(taumax)>taucr):
                return False

    if(abrb>1):
        ksb = 3.948/(abrf**2.452) +5.633
        #ksb = 0.1773*abrb**4 - 2.4181*abrb**3 + 12.044*abrb**2 - 26.253*abrb + 31.115
        if (abrb>5):
            ksb = 5.6
        for x in range(np.size(y[yb:ye])):

            taucr = taucrit(ksb,t,hb)
            taumax = taub[yb+x]

            if(abs(taumax)>taucr):
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
    abr = a/b

    ksc = 0.2354/(abr**3.299) +4.088
    #ksc = 7
    #ksc = 4
    if(a/b > 5): ksc = 4.088
    for x in range(np.size(y[yb:ye])):

        sigmacr = sigmacrit(ksc, b, t)
        sigmamax = stress[yb + x]

        if (abs(sigmamax) > sigmacr):
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
    

    K = 1
    for x in range(np.size(y[yb:ye])):

        sigmacr = colbuck(K, a)
        sigmamax = stress[yb + x]

        if (abs(sigmamax) > sigmacr):
            return False

    return True
def colbuck(K,l):
    E = 68.9 * 10**9
    sigmacr = (K*pi*pi*E*Is)/(l*l*Astring)

    return sigmacr
#-----------------------

def Marginfunc():
    y = np.linspace(0,10.1,400)

    q = np.empty(400)
    for h in range(np.size(u) - 1):

        u1 = int(u[h])
        u2 = int(u[h+1])
        print(u1)

        a = y[u2] - y[u1]
        c = 3.44 - (2* 3.44 *(0.6))/(20.2) * y[u1]    
        hf= c * 0.1121629
        hb = c * 0.058208
        abrf = a/hf
        abrb = a/hb


        if(abrf>1):
            ksf = 3.948/(abrf**2.452) +5.633

        if(abrf<1):
            ksf = 500

        if (abrf>5):
            ksf = 5.6
        
        for x in range(np.size(y[u1:u2])):
 
            taucr = taucrit(ksf,t1,hf)
            taumax = tauf[u1+x]
            mar = abs(taucr/taumax)
            global marf
            marf = np.append(marf,mar)

        if(abrb<1):
            ksb = 500
        if(abrb>1):
            ksb = 3.948/(abrf**2.452) +5.633
            #ksb = 0.1773*abrb**4 - 2.4181*abrb**3 + 12.044*abrb**2 - 26.253*abrb + 31.115
        if (abrb>5):
            ksb = 5.6
        for x in range(np.size(y[u1:u2])):

            taucr = taucrit(ksb,t1,hb)
            taumax = taub[u1+x]
            mar = taucr/taumax
            global marb
            marb = np.append(marb,mar)
    
        K = 1
        for x in range(np.size(y[u1:u2])):

            sigmacr = colbuck(K, a)
            sigmamax = sigmax[u1 + x]
            mar = float(np.real(sigmacr/sigmamax))

            global marc
            marc = np.append(marc,mar)

        b = 0.55*(3.44 - (2 * 3.44 * (0.6)) / (20.2) * y[u1])/(numstring+1)
        abr = a/b

        ksc = 0.2354/(abr**3.299) +4.088
        #ksc = 7
        #ksc = 4
        if(a/b > 5): ksc = 4.088
        for x in range(np.size(y[u1:u2])):

            sigmacr = sigmacrit(ksc, b, t2)
            sigmamax = sigmax[u1 + x]
            mar = sigmacr/sigmamax
            global mars
            mars = np.append(mars,mar)

                

    


    return


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

M = x * Aenc * 2700 * 2 * tr
print("rib weight:"+ str(np.sum(M)))
print("Total weight" + str(np.sum(M) + Vinc * 2700)) 
print("stringer thickness" + str(ts))
Marginfunc()
y = np.linspace(0,10.1,400)

#plot_margin_of_safety(marc,x)
#plot_margin_of_safety(mars,x)
#plot_margin_of_safety(marf,x)
#plot_margin_of_safety(marb,x)
marfb = np.minimum(marf,marb)
qnk = (marc,mars,marf,marb)
sig = abs((276*10**6)/sigmax) 
taf = abs((207*10**6)/(tauf))
tab = abs((207*10**6)/(taub))
marl = np.minimum(sig,taf,tab)
marfa = np.minimum(marl,marfb)
mrq = np.minimum(marc,mars,marfa)
mp = np.minimum(mrq, marf)
mp = np.minimum(mp, mars)
mp = np.minimum(mp, marb)
mp = np.minimum(mp, marc)
mp = np.minimum(mp, marl)

plot_margin_of_safety(qnk,x,['Column' ,'Skin' ,'Front Spar' ,'Rear Spar' ])
#plot_margin_of_safety([sig,taf,tab],x, ['Tensile' ,'Shear Front','Shear Back' ])
plot_margin_of_safety([mp],x,['Minimum'])
print("-------------------------------------------------------------")
print("Restarting")
print("-------------------------------------------------------------")
print("Warning watch out for memory leaks")
print("-------------------------------------------------------------")
subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])






