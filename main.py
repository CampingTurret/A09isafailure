import numpy as np
import scipy as sc
import variables
from aero_loading import *
from Inertialloads import *
from matplotlib import pyplot as plt
import os

from force_dists import *
from aerodynamic_dist import * #Import interpolated continuous distributions from data

# Constants

sf=1.5 # Safety Factor
nload=1.5*(0) # Load Factor

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

inertial_load=(fuel_load+structure_load)*nload
inertial_shear=(fuel_shear+structure_shear)*nload
inertial_moment=(fuel_moment+structure_moment)*nload

# Shear Diagram

x=np.linspace(0,10.1,sample)
x=np.append(x,10.1)

shear_dist=getShearDist(y,N_prime,sample)

# Bending Diagram

bending_dist=getBendingDist(y,shear_dist,sample)

# Torque Diagram

torque_dist=getTorqueDist(y,N_prime,M_prime,sample)

print(shear_dist)

#Sum of diagrams
sum_load = inertial_load - L_prime #n=400
sum_shear = inertial_shear + shear_dist #n=401 
sum_moment = inertial_moment + bending_dist #n=401
torque_dist+=winglet_m_torque*nload
torque_dist[400]=0

print(torque_dist)

# Plotting

# Shear Plot

shear = plt.figure(figsize=(10,5))

plt.xlim([0,11])
plt.xticks(np.arange(0, 12, 1.0))
plt.grid(True, color='0.9')

plt.axhline(y=0, color='black', linewidth=0.5, linestyle=(0,(5,5)), xmax=10.1/11)

plt.plot(x,sum_shear,color='orange')
plt.plot(x,shear_dist,color='grey',linestyle=(0,(3,5,1,5)))
plt.plot(x,inertial_shear,color='grey',linestyle=(0,(3,1,1,1)))
plt.legend(('Neutral Axis', 'Total Shear', 'Lift Shear', 'Inertial Shear'), loc="lower right")

plt.fill_between(x, sum_shear, step="pre", alpha=0.4, color='orange', hatch='|')

plt.title('Half-Span Shear Force Distribution', fontweight='bold', y=1.05)
plt.suptitle('Load Factor: '+str(round(nload,3))+'; Dynamic Pressure: '+str(int(round(q,-1)))+' Pa', y=0.92)
plt.xlabel('y [m]')
plt.ylabel('Shear Force [N]')

path=os.path.join('figures/'+str(round(nload,2))+'-'+str(int(round(q,-1))))
if os.path.exists(path) == False:
    os.mkdir(path)
plt.savefig(path+'/shear-'+str(round(nload,2))+'-'+str(int(round(q,-1)))+'.jpg')

# Bending Plot

bending = plt.figure(figsize=(10,5))

plt.xlim([0,11])
plt.xticks(np.arange(0, 12, 1.0))
plt.grid(True, color='0.9')

plt.axhline(y=0, color='black', linewidth=0.5, linestyle=(0,(5,5)), xmax=10.1/11)

plt.plot(x,sum_moment,color='purple')
plt.plot(x,bending_dist,color='grey',linestyle=(0,(3,5,1,5)))
plt.plot(x,inertial_moment,color='grey',linestyle=(0,(3,1,1,1)))
plt.legend(('Neutral Axis', 'Total Bending Moment', 'Lift Bending Moment', 'Inertial Bending Moment'), loc="upper right")

plt.fill_between(x, sum_moment, step="pre", alpha=0.4, color='purple', hatch='|')

plt.title('Half-Span Bending Moment Distribution', fontweight='bold', y=1.05)
plt.suptitle('Load Factor: '+str(round(nload,3))+'; Dynamic Pressure: '+str(int(round(q,-1)))+' Pa', y=0.92)
plt.xlabel('y [m]')
plt.ylabel('Bending Moment [Nm]')

plt.savefig(path+'/bending-'+str(round(nload,2))+'-'+str(int(round(q,-1)))+'.jpg')

# Torsion Plot

torque = plt.figure(figsize=(10,5))

plt.xlim([0,11])
plt.xticks(np.arange(0, 12, 1.0))
plt.grid(True, color='0.9')

plt.axhline(y=0, color='black', linewidth=0.5, linestyle=(0,(5,5)), xmax=10.1/11)

plt.plot(x,torque_dist,color='red')
# plt.plot(x,bending_dist,color='grey',linestyle=(0,(3,5,1,5)))
# plt.plot(x,inertial_moment,color='grey',linestyle=(0,(3,1,1,1)))
plt.legend(('Neutral Axis', 'Total Torque'), loc="upper right")

plt.fill_between(x, torque_dist, step="pre", alpha=0.4, color='red', hatch='|')

plt.title('Half-Span Torque Distribution', fontweight='bold', y=1.05)
plt.suptitle('Load Factor: '+str(round(nload,3))+'; Dynamic Pressure: '+str(int(round(q,-1)))+' Pa', y=0.92)
plt.xlabel('y [m]')
plt.ylabel('Torque [Nm]')

plt.savefig(path+'/torque-'+str(round(nload,2))+'-'+str(int(round(q,-1)))+'.jpg')

plt.show()