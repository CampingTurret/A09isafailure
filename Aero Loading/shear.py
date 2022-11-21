import numpy as np
import scipy as sp
from scipy import integrate
import variables

def getShearDist(y,dist,sample):
    
    shear_dist=np.zeros(sample)
    for i in range(sample):
        shear_dist[i]=-sp.trapz(y[i:(sample-1)],dist[i:(sample-1)])
    return shear_dist
