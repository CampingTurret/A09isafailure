import numpy as np
import scipy as sc
from variables import *


# Length L, Distributed load q, distance to shear center d1, applied load P at x1, at a distance from shear center x2, a
# distributed torque t and a torsion moment T at x2.
# t(x) = integral from x to L of [q(x)d(x)+t(x)]dx PLUS T(1-ux1(x))+P*d2(1-ux2(x))
# lift at quarter chord, weight at centroid.
# centroid is 0.465 of chord

def getTorqueDistribution(q, t, T, P):
    return sc.integrate.quad(lambda x: q * ((0.465 - 0.25) * (cr - 0.20495049505(x))) + t) + T(1 - 0.09900990099(x)) + P(0.465 - blank) * (cr - 0.20495049505(x))(1 - 0.09900990099(x))
