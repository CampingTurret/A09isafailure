import scipy as sc
import numpy as np
from variables import *
from aerodynamic_dist import cl_dist,cd_dist,cm_dist #Import interpolated continuous distributions from data

# Variables

# q0 = 100
# q1 = 100
# y=np.linspace(0,10.1,400) #Linear discretization of continuous space, sample size=400

#Force Distributions

def force_span(dist,sample,q): #Input distribution function, sample number, pressure
    y=np.linspace(0,10.1,sample) #Linear discretization of continuous space
    chord_y = (ct-cr)/b*(y)+3.44 #Chord distribution
    ddist=dist(y) #Discretized coefficient distribution
    force_dist = ddist*q*chord_y #Force distribution
    return force_dist
    
def moment_span(dist,sample,q): #Input distribution function, sample number, pressure - For moment, chord is squared
    y=np.linspace(0,10.1,sample) #Linear discretization of continuous space
    chord_y = (ct-cr)/b*(y)+3.44 #Chord Distribution
    ddist=dist(y) #Discretized coefficient distribution
    moment_dist = ddist*q*(chord_y)**2 #Moment distribution
    return moment_dist





