import numpy as np
import scipy as sp
from scipy import integrate
import variables

def getShearDist(y,dist,sample):
    
    shear_dist=np.zeros(sample)
    i=0
    for i in range(sample):
        shear_dist[i]=-sp.trapz(y[i:(sample-1)],dist[i:(sample-1)])
        print(sp.trapz(y[i:(sample-1)],dist[i:(sample-1)]))
    return shear_dist
