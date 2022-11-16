import scipy as sc
import numpy as np
import variables
from variables import *

from aerodynamic_dist import cl_dist,cd_dist,cm_dist #Import interpolated continuous distributions from data

# Variables

q0 = 100
q1 = 100
chordy = 2