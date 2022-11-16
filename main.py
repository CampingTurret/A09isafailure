import numpy as np
import scipy as sc
import variables
from matplotlib import pyplot as plt

from force_dists import *
from aerodynamic_dist import cl_dist,cd_dist,cm_dist #Import interpolated continuous distributions from data

#Vars
sample=400
q=7000

print(cd_dist(np.linspace(0,10.1,sample)))

L_prime=force_span(cl_dist,sample,q)
D_prime=force_span(cd_dist,sample,q)
M_prime=moment_span(cm_dist,sample,q)

# plt.plot(np.linspace(0,10.1,sample),L_prime)
# plt.plot(np.linspace(0,10.1,sample),D_prime)
plt.plot(np.linspace(0,10.1,sample),M_prime)
plt.show()