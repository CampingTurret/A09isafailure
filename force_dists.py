import scipy as sc
import numpy as np
import variables
from variables import *
from aerodynamic_dist import cl_dist,cd_dist,cm_dist #Import interpolated continuous distributions from data

# Variables

# q0 = 100
# q1 = 100
# y=np.linspace(0,10.1,400) #Linear discretization of continuous space, sample size=400

#Force Distributions

def force_span(dist,sample,q): #Input distribution function, sample number, pressure
    chord_y = (ct-cr)/b*(sample)+3.44 #Chord Distribution
    ddist=dist(sample)
    force_dist = ddist*q*chord_y
    return force_dist
    
def moment_span(dist,sample,q): #Input distribution function, sample number, pressure - For moment, chord is squared
    chord_y = (ct-cr)/b*(sample)+3.44 #Chord Distribution
    ddist=dist(sample)
    moment_dist = ddist*q*(chord_y)^2
    return moment_dist






