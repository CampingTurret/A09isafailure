from matplotlib import pyplot as plt
import numpy as np
from variables import b


def plot_margin_of_safety(margin_of_safety):
    # n = np.size(failure_stress)
    # print(n)
    # if n == np.size(applied_stress):
    y = np.linspace(0, b/2, np.size(margin_of_safety))
    # else:
    #     print("Applied stress and failure stress do not have the same size.")
    #     return
    # margin_of_safety = failure_stress / applied_stress\

    plt.xlim([0, 11])
    plt.xticks(np.arange(0, 12, 1.0))
    plt.grid(True, color='0.9')
    # plt.axhline(y=0, color='black', linewidth=0.5, linestyle=(0, (5, 5)), xmax=10.1 / 11)
    plt.xlabel('y [m]')
    plt.ylabel('Margin of Safety')

    plt.plot(y, margin_of_safety)
    plt.gca().set_ylim(bottom=0)

    # plt.legend(['Neutral axis', 'Margin of safety'])
    plt.legend(['Margin of safety'])

    plt.show()
    return margin_of_safety

# a = np.ones(50) * 7
# print(a)
# c = np.linspace(10, 5, 50)
# plot_margin_of_safety(a, c)
