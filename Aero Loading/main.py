import numpy as np
import scipy as sc
import variables
import shear
from shear import *
from matplotlib import pyplot as plt

from force_dists import *
from aerodynamic_dist import * #Import interpolated continuous distributions from data

# 4*0.0468**2*(t_wingbox/1.271)*(cr-cr*0.7*x/(b/2))**3

#Vars
sample=400
q=7000

# Aerodynamic Loading

y=np.linspace(0,10.1,sample)
L_prime=force_span(cl_dist0,sample,q)
D_prime=force_span(cd_dist0,sample,q)
M_prime=moment_span(cm_dist0,sample,q)

# print(getShearDist(y,L_prime,sample))

uniform=np.full(sample,4000)

plt.plot(np.linspace(0,10.1,sample),uniform)
# plt.plot(np.linspace(0,10.1,sample),D_prime)
# plt.plot(np.linspace(0,10.1,sample),M_prime)
plt.plot(np.linspace(0,10.1,sample),getShearDist(y,uniform,sample))
plt.show()