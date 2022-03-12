import matplotlib.pyplot as plt
import numpy as np
import math

def scatter_colors(parallel, legacy):
    colors = []
    for i in range(0, len(parallel)):
        if parallel[i] > legacy[i]:
            colors.append("limegreen")
        elif parallel[i] == legacy[i]:
            colors.append("black")
        else:
            colors.append("tomato")
    return colors

def scatter_log(data):
    return [math.log(v + 1) for v in data]

def scatter():
    intel_parallel = scatter_log([36.06, 0.0, 0.207, 69.324, 40.29, 0.0, 0.0, 40.335, 38.023, 0.0, 0.0, 81.21, 33.333, 0.0, 0.0, 37.093, 80.351, 0.0, 0.0, 219.323, 53.897, 0.0, 0.0, 41.975, 13917.836, 46265.756, 15033.605, 14761.15, 38355.324, 39630.807, 2200.244, 6553.521])
    intel_legacy = scatter_log([20.518, 0, 2.652, 4.262, 18.589, 0, 0.261, 1.113, 13.808, 0.266, 1.755, 2.697, 1.242, 0, 0, 13.807, 13.493, 0, 0.286, 4.14, 14.022, 0.254, 0.506, 2.271, 120.753, 101.63, 45.7, 54.111, 67.841, 81.467, 0.901, 0.302])

    nvidia_parallel = scatter_log([4429.06, 0.0, 0.0, 4192.857, 3775.842, 0.0, 0.0, 3834.402, 5880.898, 0.0, 0.0, 5308.594, 4211.527, 0.0, 0.0, 4412.081, 5629.739, 0.0, 0.0, 5421.147, 8771.87, 0.0, 0.0, 8925.991, 274083.03, 280629.653, 161385.723, 164941.252, 559958.307, 566729.968, 2300.879, 2219.738])
    nvidia_legacy = scatter_log([0.94, 0.0, 0.0, 1.415, 1.412, 0.0, 0.0, 1.176, 1.596, 0.0, 0.0, 1.642, 1.426, 0.0, 0.0, 1.405, 0.702, 0.0, 0.0, 1.415, 2.168, 0.0, 0.0, 1.623, 5.961, 6.089, 7.119, 6.064, 5.892, 6.332, 0.464, 0.475])

    m1_parallel = scatter_log([201.19, 0.0, 0.399, 205.28, 216.685, 0.0, 0.0, 185.54, 202.593, 0.324, 0.0, 218.341, 203.482, 0.0, 0.0, 200.975, 231.355, 0.0, 0.0, 258.842, 247.215, 0.541, 0.605, 242.619, 7919.699, 7948.896, 8507.024, 8635.609, 9911.99, 9545.113, 15.066, 11.55])
    m1_legacy = scatter_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 14.397, 13.847, 58.883, 59.963, 60.425, 58.727, 0.0, 0.0])

    intel_colors = scatter_colors(intel_parallel, intel_legacy)
    nvidia_colors = scatter_colors(nvidia_parallel, nvidia_legacy)
    m1_colors = scatter_colors(m1_parallel, m1_legacy)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
    ax1.scatter(intel_parallel, intel_legacy, c=intel_colors, marker="^")
    ax1.plot([-1, 15], [-1, 15], color="lightskyblue")
    ax1.set_title("Intel Iris")
    ax1.set_xlim([-1, 15])
    ax1.set_ylim([-1, 6])
    ax2.scatter(nvidia_parallel, nvidia_legacy, c=nvidia_colors, marker="^")
    ax2.plot([-1, 15], [-1, 15], color="lightskyblue")
    ax2.set_title("Nvidia")
    ax2.set_xlim([-1, 15])
    ax2.set_ylim([-1, 15])
    ax3.scatter(m1_parallel, m1_legacy, c=m1_colors, marker="^")
    ax3.plot([-1, 15], [-1, 15], color="lightskyblue")
    ax3.set_title("M1")
    ax3.set_xlim([-1, 15])
    ax3.set_ylim([-1, 15])

    fig.supxlabel("Max unsmoothed parallel instance rate")
    fig.supylabel("Max unsmoothed single instance rate")
    plt.savefig('scatter.pdf')
    #plt.show()

def scatter_rates():
    smoothed_min_rates = scatter_log([20.188, 0.0, 0.0, 27.403, 15.059, 0.0, 0.0, 18.182, 23.14, 0.0, 0.0, 32.779, 16.656, 0.0, 0.0, 12.516, 41.925, 0.0, 0.0, 108.451, 8.748, 0.0, 0.0, 9.434, 250.0, 8343.685, 7973.865, 7963.914, 8588.4, 8280.906, 0.0, 11.432])
    unsmoothed_min_rates = scatter_log([36.06, 0.0, 0.0, 69.324, 40.29, 0.0, 0.0, 40.335, 38.023, 0.0, 0.0, 81.21, 33.333, 0.0, 0.0, 37.093, 69.82, 0.0, 0.0, 196.444, 14.151, 0.0, 0.0, 16.125, 92.818, 7948.896, 7080.636, 7241.935, 9911.99, 9229.474, 0.0, 11.55])
    colors = scatter_colors(smoothed_min_rates, unsmoothed_min_rates)
    fig, ax = plt.subplots()
    ax.scatter(smoothed_min_rates, unsmoothed_min_rates, c=colors, marker="^")
    ax.plot([math.log(7.4), math.log(7.4)], [-1, 10], color="lightskyblue")
    ax.plot([-1, 10], [math.log(7.4), math.log(7.4)], color="lightskyblue")

    ax.set_title("Minimum Rates")
    ax.set_xlim([-1, 10])
    ax.set_ylim([-1, 10])
    ax.set_xlabel("Smoothed Parallel Minimum Rate")
    ax.set_ylabel("Unsmoothed Parallel Minimum Rate")
    plt.savefig("scatter_min_rates.pdf")
    #plt.show()


def do_grouping(title, ax, si, up, sp):
    labels = ['Intel Iris', 'AMD', 'Nvidia', 'M1']
    x = np.arange(len(labels))  # the label locations
    width = 0.3  # the width of the bars
    rects1 = ax.bar(x - width, si, width, label='Single Instance', color="lightcoral")
    rects2 = ax.bar(x, up, width, label='Unsmoothed Parallel', color="bisque")
    rects3 = ax.bar(x + width, sp, width, label='Smoothed Parallel', color="paleturquoise")
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title(title)
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 32)

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)

def reproducible():
    labels = ['Intel Iris', 'AMD', 'Nvidia', 'M1']
    si = [20, 0, 1, 6]
    up = [20, 28, 20, 20]
    sp = [20, 27, 20, 20]
    fig, ax = plt.subplots(constrained_layout=True)
    do_grouping("Reproducible", ax, si, up, sp)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels)
    fig.supylabel("# of Tests")
    plt.savefig('reproducible.pdf')

def grouped_bar():
    labels = ['Intel Iris', 'AMD', 'Nvidia', 'M1']
    si_sum = [11, 0, 0, 4]
    si_log_sum = [10, 0, 0, 4]
    si_ceiling_log_sum = [11, 0, 1, 6]
    up_sum = [12, 26, 19, 19]
    up_log_sum = [20, 26, 20, 20]
    up_ceiling_log_sum = [20, 28, 20, 20]
    sp_sum = [13, 25, 20, 18]
    sp_log_sum = [19, 25, 20, 20]
    sp_ceiling_log_sum = [20, 27, 20, 20]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    do_grouping("Sum", ax1, si_sum, up_sum, sp_sum)
    do_grouping("Log Sum", ax2, si_log_sum, up_log_sum, sp_log_sum)
    do_grouping("Ceiling Log Sum", ax3, si_ceiling_log_sum, up_ceiling_log_sum, sp_ceiling_log_sum)
    handles, labels = ax3.get_legend_handles_labels()
    fig.legend(handles, labels, loc = (0.865, 0.81))
    #fig.tight_layout()
    fig.supylabel("# of Tests")
    #fig.suptitle("99.999% Reproducibility Per Device")
    plt.savefig('maxed_devices.pdf')

    total_fig, ax = plt.subplots()
    total_labels = ["Single Instance", "Unsmoothed Parallel", "Smoothed Parallel"]
    sum_total_values = [0, 9, 9]
    log_sum_total_values = [0, 17, 16]
    ceiling_log_sum_total_values = [0, 19, 19]
    total_x = np.arange(len(total_labels))
    width = 0.2  # the width of the bars
    rects1 = ax.bar(total_x - width, sum_total_values, width, label='Sum', color="cornflowerblue")
    rects2 = ax.bar(total_x, log_sum_total_values, width, label='Log Sum', color="plum")
    rects3 = ax.bar(total_x + width, ceiling_log_sum_total_values, width, label='Ceiling Log Sum', color="mediumseagreen")
    ax.set_xticks(total_x, total_labels)
    ax.set_title("99.999% Reproducibility Across All Devices")
    ax.set_ylim(0, 32)
    ax.set_ylabel("# of Tests")
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)
    ax.legend()
    total_fig.tight_layout()
    #total_fig.set_size_inches(10, 8)
    #total_fig.supylabel("# of Tests")
    plt.savefig('maxed_tests.pdf')


    #plt.show()

#scatter()
#grouped_bar()
#scatter_rates()
reproducible()

