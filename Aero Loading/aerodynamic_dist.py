import scipy as sp
from scipy import interpolate  # for some reason this needs to be imported too on its own
import numpy as np
from matplotlib import pyplot as plt
from variables import CL_des
from variables import b as b_real

b = b_real - 0.01  # [m]
# Wing lift coefficients
CL0 = 0.367020  # Wing lift coefficient at AoA = 0
CL10 = 1.221274  # Wing lift coefficient at AoA = 10


# Importing result in python
folder = 'alpha_dist'
fname0 = folder + '/inducedangle_alpha=0.csv'  # Name of file with AoA=0
fname1 = folder + '/inducedangle_alpha=10.csv'  # Name of file with AoA=10
nheader = 21  # Number of header lines
nfooter = 5744  # Number of footer lines

data0 = np.genfromtxt(fname0, skip_header=nheader, skip_footer=nfooter, delimiter=',')
data1 = np.genfromtxt(fname1, skip_header=nheader, skip_footer=nfooter, delimiter=',')
# print(data1)

# Convert data to arrays for each variable
ylst = data0[:, 0]  # y coords
chordlst = data0[:, 1]  # chord lengths
# AoA = 0
Ailst0 = data0[:, 2]  # induced angle of attack
Cllst0 = data0[:, 3]  # local Cl values
ICdlst0 = data0[:, 5]  # Induced drag (Pressure drag is zero due to inviscid flow)
Cmlst0 = data0[:, 7]   # Pitching moment about the quarter-chord at that y-position.
# AoA = 10 deg
Cllst1 = data1[:, 3]  # local Cl values
ICdlst1 = data1[:, 5]  # Induced drag (Pressure drag is zero due to inviscid flow)
Cmlst1 = data1[:, 7]   # Pitching moment about the quarter-chord at that y-position.

# Ignore all values where y > halfspan and y < 0
on_wing0 = ylst <= b/2
on_wing1 = ylst > 0
on_wing = np.logical_and(on_wing0, on_wing1)  # Condition where data should be ignored
# Only look at data where condition is true, so data on wing
ylst_wing = ylst[on_wing]
chordlst_wing = chordlst[on_wing]
# AoA = 0
Ailst_wing0 = Ailst0[on_wing]
Cllst_wing0 = Cllst0[on_wing]
ICdlst_wing0 = ICdlst0[on_wing]
Cmlst_wing0 = Cmlst0[on_wing]
# AoA = 10
Cllst_wing1 = Cllst1[on_wing]
ICdlst_wing1 = ICdlst1[on_wing]
Cmlst_wing1 = Cmlst1[on_wing]

# Functions which interpolate the cl, cd and cm data at the given y coordinate (y between 0 and 10.1)
# Distributions at AoA = 0


def cl_dist0(y):
    f = sp.interpolate.interp1d(ylst_wing, Cllst_wing0, kind='cubic', fill_value='extrapolate')
    return f(y)


def cd_dist0(y):
    f = sp.interpolate.interp1d(ylst_wing, ICdlst_wing0, kind='cubic', fill_value='extrapolate')
    return f(y)


def cm_dist0(y):
    f = sp.interpolate.interp1d(ylst_wing, Cmlst_wing0, kind='cubic', fill_value='extrapolate')
    return f(y)


# Distributions at AoA = 10


def cl_dist1(y):
    f = sp.interpolate.interp1d(ylst_wing, Cllst_wing1, kind='cubic', fill_value='extrapolate')
    return f(y)


def cd_dist1(y):
    f = sp.interpolate.interp1d(ylst_wing, ICdlst_wing1, kind='cubic', fill_value='extrapolate')
    return f(y)


def cm_dist1(y):
    f = sp.interpolate.interp1d(ylst_wing, Cmlst_wing1, kind='cubic', fill_value='extrapolate')
    return f(y)


# Distributions at arbitrary lift coefficient (if it is in valid range)


def alpha(CLd=CL_des):
    sinalpha = (CLd - CL0) / (CL10 - CL0) * np.sin(np.radians(10))
    return np.arcsin(sinalpha)


def cl_dist(y, CLd=CL_des):
    lift_factor = (CLd - CL0) / (CL10 - CL0)
    Cl_dist = cl_dist0(y) + lift_factor * (cl_dist1(y) - cl_dist0(y))
    return Cl_dist, alpha


# def cd_dist(y, alpha=alpha()):
#     drag_factor = (CLd - CL0) / (CL10 - CL0)
#     Cl_dist = cl_dist0(y) + (CLd - CL0)/(CL10 - CL0) * (cl_dist1(y) - cl_dist0(y))
#     sinalpha = drag_factor * np.sin(np.radians(10))
#     alpha = np.arcsin(sinalpha)
#     return Cd_dist
#
#
# def cm_dist(y, CLd=CL_des):
#     moment_factor = (CLd - CL0) / (CL10 - CL0)
#     Cl_dist = cl_dist0(y) + (CLd - CL0)/(CL10 - CL0) * (cl_dist1(y) - cl_dist0(y))
#     sinalpha = moment_factor * np.sin(np.radians(10))
#     alpha = np.arcsin(sinalpha)
#     return Cm_dist










