import numpy as np
import scipy as sc
import variables
from aero_loading import *
import torque
from matplotlib import pyplot as plt

from force_dists import *
from aerodynamic_dist import * #Import interpolated continuous distributions from data

# 4*0.0468**2*(t_wingbox/1.271)*(cr-cr*0.7*x/(b/2))**3

#Vars
sample=400
q=7000

# Aerodynamic Loading

y=np.linspace(0,10.1,sample)
L_prime=force_span(cl_dist,sample,q)
D_prime=force_span(cd_dist,sample,q)
M_prime=moment_span(cm_dist,sample,q)
N_prime=normal_span(sample, q, CL_des)

uniform= np.full(sample,4000)

# plt.plot(np.linspace(0, 10.1, sample), L_prime)
# plt.plot(np.linspace(0, 10.1, sample), D_prime)
# plt.plot(np.linspace(0, 10.1, sample), N_prime)
# plt.plot(np.linspace(0, 10.1 ,sample), M_prime)

# Shear Diagram

shear_dist=getShearDist(y,N_prime,sample)
plt.plot(np.linspace(0,10.1,sample),shear_dist)

# Bending Diagram

bending_dist=getBendingDist(y,shear_dist,sample)
# plt.plot(np.linspace(0,10.1,sample),bending_dist)

# Torque Diagram



plt.show()
