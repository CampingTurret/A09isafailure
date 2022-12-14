import numpy as np

from margin_of_safety import plot_margin_of_safety
from main import sum_moment1
from codeinertia import sigma_y1, sigma_y2, sigma_y3
# 1-2-3, Order running from main: 26-18-15
# Positive n, negative n, zero n

# print("Sigma 1", sigma_y1)
# print("Sigma 2", sigma_y2)
# print("Sigma 3", sigma_y3)
sigma_y1 = np.abs(sigma_y1)
sigma_y2 = np.abs(sigma_y2)
sigma_y3 = np.abs(sigma_y3)


yield_strength = 276e6  # [Pa}, tensile yield strength
# print(np.size(sigma_y3))  #, np.ones(sigma_y2), np.size(sigma_y3))
failure_stress = np.ones(np.size(sigma_y1)) * yield_strength
# print(failure_stress)


margin_of_safety1 = failure_stress/sigma_y1
margin_of_safety2 = failure_stress/sigma_y2
margin_of_safety3 = failure_stress/sigma_y3

# print("MoS1:",plot_margin_of_safety(margin_of_safety1))
# print("MoS2:",plot_margin_of_safety(margin_of_safety2))
# print("MoS3:",plot_margin_of_safety(margin_of_safety3))

# print("np.minimum test", np.minimum(np.array([1,2,3]), np.array([4, -1, -5])))
margin_of_safety_lowest = np.minimum(margin_of_safety1, margin_of_safety2, margin_of_safety3)

print(margin_of_safety_lowest)
min_margin_of_safety = np.min(margin_of_safety_lowest)
if min_margin_of_safety <= 1:
    print("WATCH OUT: lowest margin of safety is", min_margin_of_safety)

plot_margin_of_safety(margin_of_safety_lowest)

