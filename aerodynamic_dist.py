import scipy as sp
from scipy import interpolate  # for some reason this needs to be imported too on its own
from scipy import integrate
import numpy as np
from matplotlib import pyplot as plt
from variables import CL_des
from variables import b as b_real

print("The code will work إن شاء الله")

# Winglet stuff on bottom of file

b = b_real  # [m]
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

def lift_factor(CLd):
    # Factor which linearly scales depending on the current wing lift coefficient wrt to lift coefficient at AoA=0
    # and AoA = 10
    return (CLd - CL0) / (CL10 - CL0)


def alpha(CLd=CL_des):
    # Returns alpha [rad] for a given wing lift coefficient (Design lift coefficient when no CL is specified)
    # RETURNS IN RADIANS
    sinalpha = lift_factor(CLd) * np.sin(np.radians(10))
    return np.arcsin(sinalpha)


def cl_dist(y, CLd=CL_des):
    # Returns local lift coefficient distribution for a given wing lift coefficient (Design lift coefficient when no
    # CL is specified)
    Cl_dist = cl_dist0(y) + lift_factor(CLd) * (cl_dist1(y) - cl_dist0(y))
    return Cl_dist


def cd_dist(y, CLd=CL_des):
    # Returns local (induced) drag coefficient distribution for a given wing lift coefficient (Design lift coefficient
    # when no CL is specified)
    Cd_dist = cd_dist0(y) + lift_factor(CLd) * (cd_dist1(y) - cd_dist0(y))
    return Cd_dist


def cm_dist(y, CLd=CL_des):
    # Returns local moment coefficient distribution for a given wing lift coefficient (Design lift coefficient when no
    # CL is specified)
    Cm_dist = cm_dist0(y) + lift_factor(CLd) * (cm_dist1(y) - cm_dist0(y))
    return Cm_dist

# print(cl_dist(np.linspace(0, b/2, 400)))
# x = np.linspace(0, b/2, 400)
# plt.plot(x, cd_dist(x, CL0))
# plt.plot(x, cd_dist(x, CL10))
# plt.plot(x, cd_dist(x))
# plt.plot(x, cl_dist(x, 20))
# plt.plot(x, cl_dist(x))
# plt.show()

# print(np.degrees(alpha(CL_des)))

# WINGLET STUFF:


# Ignore all values where y is not on winglet
on_winglet = ylst > b/2 + 0.03
# Only look at data where condition is true, so data on wing
ylst_winglet = ylst[on_winglet]
chordlst_winglet = chordlst[on_winglet]
# print(chordlst_winglet)
# AoA = 0
Cllst_winglet0 = Cllst0[on_winglet]
ICdlst_winglet0 = ICdlst0[on_winglet]
Cmlst_winglet0 = Cmlst0[on_winglet]
# AoA = 10
Cllst_winglet1 = Cllst1[on_winglet]
ICdlst_winglet1 = ICdlst1[on_winglet]
Cmlst_winglet1 = Cmlst1[on_winglet]


# Functions which interpolate the cl, cd and cm data at the given y coordinate (y between 0 and 10.1)
# Distributions at AoA = 0
# print(Cllst_winglet0)

def cl_winglet_dist0(y):
    f = sp.interpolate.interp1d(ylst_winglet, Cllst_winglet0, kind='cubic', fill_value='extrapolate')
    return f(y)


def cd_winglet_dist0(y):
    f = sp.interpolate.interp1d(ylst_winglet, ICdlst_winglet0, kind='cubic', fill_value='extrapolate')
    return f(y)


def cm_winglet_dist0(y):
    f = sp.interpolate.interp1d(ylst_winglet, Cmlst_winglet0, kind='cubic', fill_value='extrapolate')
    return f(y)


# Distributions at AoA = 10


def cl_winglet_dist1(y):
    f = sp.interpolate.interp1d(ylst_winglet, Cllst_winglet1, kind='cubic', fill_value='extrapolate')
    return f(y)


def cd_winglet_dist1(y):
    f = sp.interpolate.interp1d(ylst_winglet, ICdlst_winglet1, kind='cubic', fill_value='extrapolate')
    return f(y)


def cm_winglet_dist1(y):
    f = sp.interpolate.interp1d(ylst_winglet, Cmlst_winglet1, kind='cubic', fill_value='extrapolate')
    return f(y)


CL0_winglet, err0 = sp.integrate.quad(cl_winglet_dist0, min(ylst_winglet), max(ylst_winglet))
# print(CL0_winglet)
CL10_winglet, err1 = sp.integrate.quad(cl_winglet_dist1, min(ylst_winglet), max(ylst_winglet))
# print(CL10_winglet)

# Distributions at arbitrary lift coefficient (if it is in valid range)


# def winglet_lift_factor(CLd):
#     # Factor which linearly scales depending on the current wing lift coefficient wrt to lift coefficient at AoA=0
#     # and AoA = 10
#     return (CLd - CL0_winglet) / (CL10_winglet - CL0_winglet)


def cl_winglet_dist(y, CLd=CL_des):
    # Returns local lift coefficient distribution for a given wing lift coefficient (Design lift coefficient when no
    # CL is specified)
    Cl_dist = cl_winglet_dist0(y) + lift_factor(CLd) * (cl_winglet_dist1(y) - cl_winglet_dist0(y))
    return Cl_dist


def cd_winglet_dist(y, CLd=CL_des):
    # Returns local (induced) drag coefficient distribution for a given wing lift coefficient (Design lift coefficient
    # when no CL is specified)
    Cd_dist = cd_winglet_dist0(y) + lift_factor(CLd) * (cd_winglet_dist1(y) - cd_winglet_dist0(y))
    return Cd_dist


def cm_winglet_dist(y, CLd=CL_des):
    # Returns local moment coefficient distribution for a given wing lift coefficient (Design lift coefficient when no
    # CL is specified)
    Cm_dist = cm_winglet_dist0(y) + lift_factor(CLd) * (cm_winglet_dist1(y) - cm_winglet_dist0(y))
    return Cm_dist

# print(cm_winglet_dist(0))
# y = np.linspace(b/2, b/2+1.4, 400)
# print(cd_winglet_dist(y))

# CL_winglet, err = sp.integrate.quad(cl_winglet_dist, min(ylst_winglet), max(ylst_winglet))
# print(CL_winglet, err)

