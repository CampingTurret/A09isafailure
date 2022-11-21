import numpy as np
import scipy as sc
from variables import *

# Length L, Distributed load q, distance to shear center d1, applied load P at x1, at a distance from shear center x2, a
# distributed torque t and a torsion moment T at x2.
# t(x) = integral from x to L of [q(x)d(x)+t(x)]dx PLUS T(1-ux1(x))+P*d2(1-ux2(x))

def tau(x):
    return sc.integrate.quad(lambda x: q(x)*d(x)+t(x), x, b/2) +