from matplotlib import pyplot as plt
import numpy as np
from variables import b


def plot_margin_of_safety(margin_of_safety, bays=False):
    # n = np.size(failure_stress)
    # print(n)
    # if n == np.size(applied_stress):
    y = np.linspace(0, b / 2, np.size(margin_of_safety[0]))
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

    if bays is not False:
        np.delete(margin_of_safety, 0)
        bays_pos = bays * y
        #plt.bar(y, bays*max_MoS, color='0.4', width=0.08, label='Ribs')
        plt.axvline(0, color='0.7', linestyle=(0, (5, 5)), label='Ribs')
        for bay in bays_pos:
            if bay != 0:
                plt.axvline(bay, linewidth=1, color='0.7', linestyle=(0,(5,5)))
        # plt.vlines(bays_pos, ymin=0, ymax=1, colors='0.4', label='Ribs', linestyles=(0,(5,5)))

    for MoS in margin_of_safety:
        plt.plot(y, MoS, label='Margin of safety')
    plt.gca().set_ylim(bottom=0)

    # plt.legend(['Neutral axis', 'Margin of safety'])
    plt.legend()

    plt.show()
    return margin_of_safety


# c = np.linspace(10, 5, 400)
# d = np.zeros(400)
# d[15], d[50], d[160], d[300], d[-1] = 1, 1, 1, 1, 1
# plot_margin_of_safety(c, d)


