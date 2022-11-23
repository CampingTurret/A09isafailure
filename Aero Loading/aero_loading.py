import numpy as np
import scipy as sp
from variables import *
from force_dists import normal_winglet
from funcmodule import yMAC

winglet_force = normal_winglet(400, 7000)

def getWingletForce(winglet_force):
    
    ymac_wlt = yMAC(wlt_span,wlt_cr,wlt_ct) # Obtain location of winglet MAC
    wlt_y = b/2*np.cos(np.deg2rad(gamma))+ymac_wlt*np.cos(np.deg2rad(wlt_gamma)) # Obtain location of vertical force component
    wlt_force_y = winglet_force*np.sin(wlt_gamma) # Obtain vertical force components
    # print(wlt_force_y)
    
    return wlt_force_y

def getWingletMoment(winglet_force): # Calculate Moment due to Winglet
    
    ymac_wlt = yMAC(wlt_span,wlt_cr,wlt_ct) # Obtain location of winglet MAC
    
    wlt_z = b/2*np.sin(np.deg2rad(gamma))+ymac_wlt*np.sin(np.deg2rad(wlt_gamma)) # Obtain z and y moment arm lengths
    wlt_y = b/2*np.cos(np.deg2rad(gamma))+ymac_wlt*np.cos(np.deg2rad(wlt_gamma))
    
    wlt_force_z = winglet_force*np.cos(wlt_gamma)  
    wlt_force_y = winglet_force*np.sin(wlt_gamma)
    
    winglet_moment = wlt_z*wlt_force_z + wlt_y*wlt_force_y # Calculate moment (sum of z and y components)
    print(winglet_moment)
    
    return winglet_moment

def getShearDist(y,dist,sample): # Obtains the shear distribution of the wing
    
    shear_dist=np.zeros(sample+1) # Creates array
    winglet_shear = getWingletForce(winglet_force)
    i=0
    for i in range(sample): # Numerical integration for each point in data (Bounds: [x,L])
        shear_dist[i]=-sp.trapz(dist[i:(sample-2)],y[i:(sample-2)])-winglet_shear
        # print(sp.trapz(y[i:(sample-1)],dist[i:(sample-1)]))
        shear_dist[400]=0
    print(shear_dist)
    return shear_dist

def getBendingDist(y,dist,sample): # Obtains the bending distribution of the wing
    
    bend_dist=np.zeros(sample+1) # Creates array
    winglet_moment = getWingletMoment(winglet_force)
    i=0
    for i in range(sample): # Numerical integration for each point in data (Bounds: [x,L])
        bend_dist[i]=-sp.trapz(dist[i:(sample-2)],y[i:(sample-2)])+winglet_moment
        # print(sp.trapz(y[i:(sample-1)],dist[i:(sample-1)]))
        bend_dist[400]=0
    return bend_dist