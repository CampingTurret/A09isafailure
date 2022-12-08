import numpy as np
# from codeinertia import airfoilparameters as afp
from math import pi

# constants
# y = np.linspace(0.0, 10.1, 400)
c_r = 3.44  # chord root
ws = 20.2  # wingspan
E = 68.9 * 10**9
# c = c_r - 0.6*y*2/ws*c_r
v = 0.33
# n_str = 1

def sigmacrit(a_start, y, t, n_str):

    # h1, h2, w1, w2, A = airfoilparameters(0.2, 0.75)

    c = c_r - 0.6*y*2/ws*c_r
    b = 0.55*c/(n_str + 1)
    a = y - a_start
    k_c = 3.277*(b**2)/(a**2)+7.125

    sigma = (pi**2*k_c*E*(t**2))/(12*(1-v**2)*b**2)

    return sigma

