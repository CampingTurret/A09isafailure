import numpy as np
# from codeinertia import airfoilparameters as afp
from math import pi
from codeinertia import

# constants
# y = np.linspace(0.0, 10.1, 400)
c_r = 3.44  # chord root
ws = 20.2  # wingspan
E = 68.9 * 10**9
# c = c_r - 0.6*y*2/ws*c_r
v = 0.33
# n_str = 1

def sigmacrit(k_c, b, t):

    # h1, h2, w1, w2, A = airfoilparameters(0.2, 0.75)

    sigma = (pi**2*k_c*E*(t**2))/(12*(1-v**2)*b**2)

    return sigma


def check2(ye, yb, t, y, stress):
    a = y[ye] - y[yb]
    b = 0.55*(3.44 - (2 * 3.44 * (0.6)) / (20.2) * y[yb])
    ksc = 3.178*(b**2.082)/(a**2)+7.173

    for x in range(np.size(y[yb:ye])):

        sigmacr = sigmacrit(ksc, b, t)
        sigmamax = stress[yb + x]

        if (sigmamax > sigmacr):
            return False

    return True


def skinsearch(ystart, stress):
    yindex = ystart
    t = t1

    y = np.linspace(0.0, 10.1, 400)
    continu = True

    while (continu):

        continu = check2(yindex, ystart, t, y, stress)
        print(yindex)
        yindex = yindex + 1

        if (yindex > 399):
            return 399

    yend = yindex - 1

    return yend
