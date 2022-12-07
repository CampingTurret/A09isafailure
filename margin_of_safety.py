from matplotlib import pyplot as plt
import numpy as np
from variables import b


def plot_margin_of_safety(failure_stress, applied_stress):
    n = np.size(failure_stress)
    if n == np.size(applied_stress):
        y = np.linspace(0, b/2, n)
    else:
        print("Applied stress and failure stress do not have the same size.")
        return
    margin_of_safety = failure_stress / applied_stress
    plt.show(y, margin_of_safety)
    return
