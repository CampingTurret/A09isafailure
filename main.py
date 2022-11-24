import numpy as np
import scipy as sc
import variables
from aero_loading import *
from Inertialloads import *
from matplotlib import pyplot as plt

from force_dists import *
from aerodynamic_dist import * #Import interpolated continuous distributions from data

#Vars


# Aerodynamic Loading

y=np.linspace(0,10.1,sample)
L_prime=force_span(cl_dist,sample,q)
D_prime=force_span(cd_dist,sample,q)
M_prime=moment_span(cm_dist,sample,q)
N_prime=normal_span(sample, q, CL_des)

# uniform= np.full(sample,4000)

# plt.plot(np.linspace(0, 10.1, sample), L_prime)
# plt.plot(np.linspace(0, 10.1, sample), D_prime)
# plt.plot(np.linspace(0, 10.1, sample), N_prime)
# plt.plot(np.linspace(0, 10.1 ,sample), M_prime)

# Inertial Loading

fuel_load=np.zeros(400)
fuel_shear=np.zeros(401)
fuel_moment=np.zeros(401)
structure_load=np.zeros(400)
structure_shear=np.zeros(401)
structure_moment=np.zeros(401)
a=generatearray(b)

wlt_weight = wingletweight(m1,wing_vol,wlt_vol)
structure_density=structuredensity(m1, wlt_weight, b, a, cr, taper)
winglet_m_torque=winglettorque(wlt_weight,g,taper,cr)

fuel_vol = fuelvolume(wbx_frac,cr,b,taper)

i=0
for i in range(sample):
    fuel_load[i]=fuelloading(fuel_density,g,wbx_frac,cr,b,taper,y[i])
    fuel_shear[i]=fuelshear(fuel_density,g,wbx_frac,cr,b,taper,y[i])
    fuel_moment[i]=fuelmoment(fuel_density,g,wbx_frac,cr,b,taper,y[i])
    
    structure_load[i]=structureloading(y[i],a,structure_density,g,cr,b,taper)
    structure_shear[i]=structureshear(y[i],a,structure_density,g,cr,b,taper,wlt_weight)
    structure_moment[i]=structureMoment(y[i],a,structure_density,g,cr,b,taper,wlt_weight)

# print(fuel_load)
print(structure_shear)

inertial_load=fuel_load+structure_load
inertial_shear=fuel_shear+structure_shear
inertial_moment=fuel_moment+structure_moment



# Shear Diagram

x=np.linspace(0,10.1,sample)
x=np.append(x,10.1)



shear_dist=getShearDist(y,N_prime,sample)
#plt.plot(x,shear_dist)

# Bending Diagram

bending_dist=getBendingDist(y,shear_dist,sample)
#plt.plot(x,bending_dist)

# Torque Diagram

torque_dist=getTorqueDist(y,N_prime,M_prime,sample)
# plt.plot(x,torque_dist)

#Sum of diagrams
sum_load= inertial_load + L_prime
sum_shear= inertial_shear + shear_dist
sum_moment = inertial_moment + bending_dist
sum_torque = torque_dist + winglet_m_torque




# Plotting

# ld, (ax1, ax2) = plt.subplots(1, 2)
# ax1.plot(np.linspace(0,10.1,sample),shear_dist)
# ax2.plot(np.linspace(0,10.1,sample),bending_dist)
plt.show()