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

nload1=sf*2.609587504
CL1 = sf*0.147668144

nload2=sf*0   #2.609587504              # (float(input("Load Factor [-]: "))) # Load Factor
CL2 = sf*0    #0.133858438               #(float(input("Lift Coefficient C_L [-]: "))) # CL

q3=24658.91887
nload3=sf*-1
CL3 = sf*-0.137881146

y=np.linspace(0,10.1,sample)
x=np.linspace(0,10.1,sample)
x=np.append(x,10.1)

print("Calculating loading...\n")

def calcForces(sf,nload,q,CL):

    # Aerodynamic Loading

    y=np.linspace(0,10.1,sample)
    L_prime=force_span(cl_dist,sample,q, CL) #* nload
    D_prime=force_span(cd_dist,sample,q, CL) #* nload
    M_prime=moment_span(cm_dist,sample,q, CL) #* nload
    N_prime=normal_span(sample, q, CL) #* nload

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

    fuelcheck=float(input("Fuel Percentage: "))
    fuel_load=fuel_load*fuelcheck/100
    fuel_shear=fuel_shear*fuelcheck/100
    fuel_moment=fuel_moment*fuelcheck/100
    # print(fuel_load)

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

    torque_dist=getTorqueDist(y,N_prime,M_prime,sample) # print(torque_dist)

    ######## Final Distributions

    sum_load = inertial_load - L_prime #n=400
    sum_shear = inertial_shear + shear_dist #n=401
    sum_moment = inertial_moment + bending_dist #n=401
    torque_dist+=winglet_m_torque*nload
    torque_dist[400]=0
    
    plt.show()
    
    return sum_load,sum_shear,sum_moment,torque_dist,shear_dist,inertial_shear,bending_dist,inertial_moment

sum_load1,sum_shear1,sum_moment1,torque_dist1,lift_shear1,inertial_shear1,lift_moment1,inertial_moment1=calcForces(1.5,nload1,q,CL1)
sum_load2,sum_shear2,sum_moment2,torque_dist2,lift_shear2,inertial_shear2,lift_moment2,inertial_moment2=calcForces(1.5,nload2,q,CL2)
sum_load3,sum_shear3,sum_moment3,torque_dist3,lift_shear3,inertial_shear3,lift_moment3,inertial_moment3=calcForces(1.5,nload3,q3,CL3)

# Plotting

def plot(x,sum_shear,lift_shear,inertial_shear,sum_moment,lift_moment,inertial_moment,sum_torque,nload,q):

    # Shear Plot

    shear = plt.figure(figsize=(10,5))

    plt.xlim([0,11])
    plt.xticks(np.arange(0, 12, 1.0))
    plt.grid(True, color='0.9')

    plt.axhline(y=0, color='black', linewidth=0.5, linestyle=(0,(5,5)), xmax=10.1/11)

    plt.plot(x,sum_shear,color='orange')
    plt.plot(x,lift_shear,color='grey',linestyle=(0,(3,5,1,5)))
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
    plt.plot(x,lift_moment,color='grey',linestyle=(0,(3,5,1,5)))
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

    plt.plot(x,sum_torque,color='red')
    # plt.plot(x,bending_dist,color='grey',linestyle=(0,(3,5,1,5)))
    # plt.plot(x,inertial_moment,color='grey',linestyle=(0,(3,1,1,1)))
    plt.legend(('Neutral Axis', 'Total Torque'), loc="lower right")

    plt.fill_between(x, sum_torque, step="pre", alpha=0.4, color='red', hatch='|')

    plt.title('Half-Span Torque Distribution', fontweight='bold', y=1.05)
    plt.suptitle('Load Factor: '+str(round(nload,3))+'; Dynamic Pressure: '+str(int(round(q,-1)))+' Pa', y=0.92)
    plt.xlabel('y [m]')
    plt.ylabel('Torque [Nm]')

    plt.savefig(path+'/torque-'+str(round(nload,2))+'-'+str(int(round(q,-1)))+'.jpg')

    plt.show()
    
# plot(x,sum_shear1,lift_shear1,inertial_shear1,sum_moment1,lift_moment1,inertial_moment1,torque_dist1,nload1,q)
# plot(x,sum_shear2,lift_shear2,inertial_shear2,sum_moment2,lift_moment2,inertial_moment2,torque_dist2,nload2,q)
# plot(x,sum_shear3,lift_shear3,inertial_shear3,sum_moment3,lift_moment3,inertial_moment3,torque_dist3,nload3,q3)