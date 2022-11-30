import numpy as np
import scipy as sp
from variables import *
from force_dists import normal_winglet,tangential_winglet,moment_winglet
from funcmodule import yMAC

winglet_force = normal_winglet(sample, q)

def getWingletForce(winglet_force):
    
    ymac_wlt = yMAC(wlt_span,wlt_cr,wlt_ct) # Obtain location of winglet MAC
    wlt_y = b/2*np.cos(np.deg2rad(gamma))+ymac_wlt*np.cos(np.deg2rad(wlt_gamma)) # Obtain location of vertical force component
    wlt_force_y = winglet_force*np.sin(wlt_gamma) # Obtain vertical force components
    print(wlt_force_y)
    
    return wlt_force_y

def getWingletMoment(y,winglet_force): # Calculate Moment due to Winglet
    
    ymac_wlt = yMAC(wlt_span,wlt_cr,wlt_ct) # Obtain location of winglet MAC
    
    winglet_moment = np.zeros(sample+1)
    
    wlt_z = (b/2-y*np.sin(np.deg2rad(gamma)))*np.sin(np.deg2rad(gamma))+ymac_wlt*np.sin(np.deg2rad(wlt_gamma)) # Obtain z and y moment arm lengths
    wlt_y = (b/2-y*np.cos(np.deg2rad(gamma)))*np.cos(np.deg2rad(gamma))+ymac_wlt*np.cos(np.deg2rad(wlt_gamma))
    
    # print
    
    wlt_force_z = winglet_force*np.cos(wlt_gamma)  
    wlt_force_y = winglet_force*np.sin(wlt_gamma)
    
    winglet_moment = wlt_z*wlt_force_z + wlt_y*wlt_force_y # Calculate moment (sum of z and y components)
    # print(winglet_moment)
    
    return winglet_moment

def getWingletTorque(winglet_drag, winglet_force):
    
    # Geometric Calculations
    mac_wlt = (2/3)*wlt_cr*(1+(wlt_taper)+(wlt_taper)**2)/(1+(wlt_taper))
    ymac_wlt = yMAC(wlt_span,wlt_cr,wlt_ct) # Obtain location of winglet MAC
    wlt_z = b/2*np.sin(np.deg2rad(gamma))+ymac_wlt*np.sin(np.deg2rad(wlt_gamma))
    
    wlt_le_sweep = np.arcsin((1.8-wlt_le_offset)/(wlt_span/2))
    xmac=ymac_wlt*np.tan(wlt_le_sweep)
    ac_wlt=xmac+0.25*mac_wlt
    ac_wlt_offset=ac_wlt+wlt_le_offset
    
    ltorque_arm = cr*0.465-ac_wlt_offset # Torque arm for lift
    
    # print("torque arm: "+str(ltorque_arm))
    
    # Due to drag
    drag=tangential_winglet(sample,q)
    
    # Due to lift
    wlt_force_y = winglet_force*np.sin(wlt_gamma)
    
    # Final torque due to winglet
    winglet_torque=wlt_z*drag-moment_winglet(sample, q)+wlt_force_y*ltorque_arm
    
    return winglet_torque

def getShearDist(y,dist,sample): # Obtains the shear distribution of the wing
    
    shear_dist=np.zeros(sample+1) # Creates array
    winglet_shear = getWingletForce(winglet_force)
    i=0
    for i in range(sample): # Numerical integration for each point in data (Bounds: [x,L])
        shear_dist[i]=-sp.trapz(dist[i:(sample-2)],y[i:(sample-2)])-winglet_shear
        # print(sp.trapz(y[i:(sample-1)],dist[i:(sample-1)]))
        shear_dist[400]=0
    # print(shear_dist)
    return shear_dist

def getBendingDist(y,dist,sample): # Obtains the bending distribution of the wing
    
    bend_dist=np.zeros(sample+1) # Creates array
    winglet_moment = getWingletMoment(y, winglet_force)
    # winglet_moment[400]=0
    i=0
    for i in range(sample): # Numerical integration for each point in data (Bounds: [x,L])
        bend_dist[i]=-sp.trapz(dist[i:(sample-2)],y[i:(sample-2)])+winglet_moment[i]
        # print(sp.trapz(y[i:(sample-1)],dist[i:(sample-1)]))
        bend_dist[400]=0
    # bend_dist+=winglet_moment
    return bend_dist

def getTorqueDist(y,ldist,mdist,sample):
    
    torque_dist=np.zeros(sample+1) # Creates array
    winglet_torque=getWingletTorque(tangential_winglet(sample,q),winglet_force)
    
    # Calculate spanwise distance of AC to CoG
    dx=np.zeros(sample)
    j=0
    for j in range(sample):
        # print(y[j])
        dx[j]=((0.465-0.25)*(cr-0.20495049505*(y[j])))
        # print(dx[j])
        
    i=0
    # print(winglet_torque) 
    for i in range(sample): # Numerical integration for each point in data (Bounds: [x,L])
        torque_dist[i]=sp.trapz(ldist[i:(sample-2)]*dx[i:(sample-2)]+mdist[i:(sample-2)],y[i:(sample-2)])+winglet_torque
        
        torque_dist[400]=0
    # print(torque_dist)
    return torque_dist