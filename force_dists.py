import scipy as sc
import numpy as np
import variables
from variables import *

from aerodynamic_dist import cl_dist,cd_dist,cm_dist #Import interpolated continuous distributions from data

# Variables

q0 = 100
q1 = 100
y=np.linspace(0,10.1,400) #Linear discretization of continuous space, sample size=400

chord_y = (ct-cr)/b*(y)+3.44 #Chord Distribution

#Force Distributions

CL_span=cl_dist(y)
CD_span=cd_dist(y)
CM_span=cm_dist(y)

Lprime = CL_span*q0*chord_y
Dprime = CD_span*q0*chord_y
Mprime = CM_span*q0*(chord_y)^2
