import scipy as sp
from scipy import interpolate  # for some reason this needs to be imported too on its own
import numpy as np
from matplotlib import pyplot as plt

#ALL FOR AOA=0 RIGHT NOW

# Importing result in python
folder = 'alpha_dist'
fname = folder + '/inducedangle_alpha=0.csv'  # Name of file
nheader = 21  # Number of header lines
nfooter = 5744  # Number of footer lines

data = np.genfromtxt(fname, skip_header=nheader, skip_footer=nfooter, delimiter=',')
#print(data)

# Convert data to arrays for each variable
ylst = data[:, 0]  # y coords
chordlst = data[:, 1]  # chord lengths
Ailst = data[:, 2]  # induced angle of attack
Cllst = data[:, 3]  # local Cl values
ICdlst = data[:, 5]  # Induced drag (Pressure drag is zero due to inviscid flow)
Cmlst = data[:, 7]   # Pitching moment about the quarter-chord at that y-position.

b = 20.19  # [m]

# Ignore all values where y > halfspan and y < 0
on_wing0 = ylst <= b/2
on_wing1 = ylst > 0
on_wing = np.logical_and(on_wing0, on_wing1)  # Condition where data should be ignored
# Only look at data where condition is true, so data on wing
ylst_wing = ylst[on_wing]
chordlst_wing = chordlst[on_wing]
Ailst_wing = Ailst[on_wing]
Cllst_wing = Cllst[on_wing]
ICdlst_wing = ICdlst[on_wing]
Cmlst_wing = Cmlst[on_wing]

# Functions which interpolate the cl, cd and cm data at the given y coordinate (y between 0 and 10.1)


def cl_dist(y):
    f = sp.interpolate.interp1d(ylst_wing, Cllst_wing, kind='cubic', fill_value='extrapolate')
    return f(y)


def cd_dist(y):
    f = sp.interpolate.interp1d(ylst_wing, ICdlst_wing, kind='cubic', fill_value='extrapolate')
    return f(y)


def cm_dist(y):
    f = sp.interpolate.interp1d(ylst_wing, Cmlst_wing, kind='cubic', fill_value='extrapolate')
    return f(y)











