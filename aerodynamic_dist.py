import scipy as sp
import numpy as np

# Importing result in python
fname = 'abc.dat'  # Name of file
nheader = 15  # Number of header lines
nfooter = 69  # Number of footer lines

data = np.genfromtxt(fname, skip_header=nheader, skip_footer=nfooter)
print(data)

# Convert data to arrays for each variable
ylst = data[:, 0]  # y coords
chordlst = data[:, 1]  # chord lengths
Ailst = data[:, 2]  # induced angle of attack
Cllst = data[:, 3]  # local Cl values

