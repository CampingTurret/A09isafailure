import numpy as np
import scipy as sp
import variables

def getBendingDist(y,dist,sample):
    
    bend_dist=np.zeros(sample)
    i=0
    for i in range(sample):
        bend_dist[i]=-sp.trapz(dist[i:(sample-1)],y[i:(sample-1)])
        # print(sp.trapz(y[i:(sample-1)],dist[i:(sample-1)]))
    return bend_dist

def getShearDist(y,dist,sample):
    
    shear_dist=np.zeros(sample)
    i=0
    for i in range(sample):
        shear_dist[i]=-sp.trapz(dist[i:(sample-1)],y[i:(sample-1)])
        # print(sp.trapz(y[i:(sample-1)],dist[i:(sample-1)]))
    return shear_dist