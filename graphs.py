import matplotlib.pyplot as plt
import numpy as np
import math


def max_rate_for_device(title, ax, si_no_stress, si, parallel_no_stress, up, sp, set_xticks=False):
    labels = ["Message Passing Default", "Message Passing Barrier Variant 1", "Message Passing Barrier Variant 2", "Message Passing Coherency", "Store Default", "Store Barrier Variant 1", "Store Barrier Variant 2", "Store Coherency", "Read RMW", "Read RMW Barrier 1", "Read RMW Barrier 2", "Read Coherency", "Load Buffer Default", "Load Buffer Barrier Variant 1", "Load Buffer Barrier Variant 2", "Load Buffer Coherency", "Store Buffer RMW", "Store Buffer RMW Barrier 1", "Store Buffer RMW Barrier 2", "Store Buffer Coherency", "2+2 Write RMW", "2+2 Write RMW Barrier 1", "2+2 Write RMW Barrier 2", "2+2 Write Coherency", "RR Mutations Default", "RR Mutations RMW", "RW Mutations Default", "RW Mutations RMW", "WR Mutations Default", "WR Mutations RMW", "WW Mutations Default", "WW Mutations RMW"]
    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars
    ax.bar(x - 2 * width, si_no_stress, width, label='Single Instance No Stress', color="bisque")
    ax.bar(x - width, si, width, label='Single Instance', color="lightcoral")
    ax.bar(x, parallel_no_stress, width, label='Parallel No Stress', color="paleturquoise")
    ax.bar(x + width, up, width, label='Unsmoothed Parallel', color="plum")
    ax.bar(x + 2 * width, sp, width, label='Smoothed Parallel', color="seagreen")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title(title)
    if set_xticks:
        ax.set_xticks(x, labels, rotation=45, fontsize=6)
    else:
        ax.set_xticks([], [])

def means():
    labels = ["Intel", "AMD", "Nvidia", "M1"]
    si_no_stress_means = take_log([0, 0, 0, 0, 0, 0, 0, 0, 9.693, 0, 0, 0])
    si_means = take_log([4.87, 9.429, 0.458, 0, 4.715, 22.295, 1.446, 0, 59.088, 53.378, 4.8, 33.28])
    parallel_no_stress_means = take_log([3.628, 0, 316.912, 0, 47.859, 0, 990.374, 0, 8007.971, 0, 354670.514, 0])
    parallel_means = take_log([15.676, 6994.569, 1816.608, 72.466, 81.543, 25100.945, 5349.179, 218.6, 22089.78, 58313.47, 251531.069, 6561.868])
    x = np.arange(len(labels))
    width = 0.2
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6), constrained_layout=True)
    ax1.bar(x - 1.5 * width, si_no_stress_means[0:4], width, label="Single Instance No Stress")
    ax1.bar(x - .5 * width, si_means[0:4], width, label="Single Instance")
    ax1.bar(x + .5 * width, parallel_no_stress_means[0:4], width, label="Parallel No Stress")
    ax1.bar(x + 1.5 * width, parallel_means[0:4], width, label="Parallel")
    ax1.set_ylim([0, 7])
    ax1.set_xticks(x, labels)
    ax1.set_title("Weakening sw")
    ax2.bar(x - 1.5 * width, si_no_stress_means[4:8], width)
    ax2.bar(x - .5 * width, si_means[4:8], width)
    ax2.bar(x + .5 * width, parallel_no_stress_means[4:8], width)
    ax2.bar(x + 1.5 * width, parallel_means[4:8], width)
    ax2.set_ylim([0, 7])
    ax2.set_xticks(x, labels)
    ax2.set_title("Weakening po")
    ax3.bar(x - 1.5 * width, si_no_stress_means[8:12], width)
    ax3.bar(x - .5 * width, si_means[8:12], width)
    ax3.bar(x + .5 * width, parallel_no_stress_means[8:12], width)
    ax3.bar(x + 1.5 * width, parallel_means[8:12], width)
    ax3.set_ylim([0, 7])
    ax3.set_xticks(x, labels)
    ax3.set_title("Reversing po")
    fig.supylabel("Average of Rates of Weak Behaviors Per Second (Log Scale)", fontsize=10)
    fig.legend(loc=(0.8, 0.8))
    plt.savefig("figure1.pdf")



def max_rate_per_test():
    intel_si_weak = []
    intel_si_no_stress = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 66.318, 10.412, 0.0, 0.0, 0.812, 0.0, 0.0, 0.0])
    intel_si = take_log([20.518, 0, 2.652, 4.262, 18.589, 0, 0.261, 1.113, 13.808, 0.266, 1.755, 2.697, 1.242, 0, 0, 13.807, 13.493, 0, 0.286, 4.14, 14.022, 0.254, 0.506, 2.271, 120.753, 101.63, 45.7, 54.111, 67.841, 81.467, 0.901, 0.302])
    intel_parallel_no_stress = take_log([2.855, 0.0, 0.0, 24.879, 1.417, 0.0, 0.0, 10.197, 6.653, 0.0, 0.0, 71.924, 0.0, 0.0, 0.0, 9.091, 48.193, 0.0, 0.0, 162.2, 6.194, 0.0, 0.0, 8.862, 3617.812, 14827.083, 4303.371, 3815.556, 19325.039, 18061.719, 56.733, 56.457])
    intel_up = take_log([36.06, 0.0, 0.207, 69.324, 40.29, 0.0, 0.0, 40.335, 38.023, 0.0, 0.0, 81.21, 33.333, 0.0, 0.0, 37.093, 80.351, 0.0, 0.0, 219.323, 53.897, 0.0, 0.0, 41.975, 13917.836, 46265.756, 15033.605, 14761.15, 38355.324, 39630.807, 2200.244, 6553.521])
    intel_sp = take_log([20.188, 0.0, 0.0, 27.403, 15.059, 0.0, 0.0, 18.182, 23.14, 0.0, 0.0, 32.779, 16.656, 0.0, 0.0, 12.516, 41.925, 0.0, 0.0, 108.451, 22.261, 0.0, 0.0, 25.132, 8184.632, 37802.657, 11810.376, 11368.64, 37637.563, 34749.518, 1702.151, 3986.056])

    amd_si_no_stress = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    amd_si = take_log([3.538, 0.0, 0.419, 1.72, 52.795, 0.0, 9.742, 50.66, 0.0, 0.0, 0.0, 0.0, 82.527, 3.831, 7.987, 77.117, 0.0, 0.0, 0.0, 0.0, 8.887, 0.0, 0.0, 4.275, 0.0, 77.384, 79.592, 83.377, 64.516, 122.152, 0.0, 0.0])
    amd_parallel_no_stress = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    amd_up = take_log([32743.98, 17074.334, 6030.624, 33700.394, 2318.066, 7.092, 30.762, 2305.777, 22185.987, 6371.891, 6290.766, 21687.003, 881.778, 2.964, 11.34, 867.438, 20047.436, 6035.156, 5841.646, 92015.089, 27.656, 0.755, 0.0, 29.969, 92.818, 66496.112, 40928.654, 33179.554, 305266.176, 20469.12, 0.0, 75.325])
    amd_sp = take_log([31573.813, 15775.885, 10634.86, 29845.088, 1527.188, 2.681, 16.108, 1234.794, 20997.481, 6919.654, 8094.089, 20847.458, 574.794, 2.286, 7.982, 571.93, 19325.758, 7567.145, 7102.015, 96098.315, 18.831, 1.311, 0.0, 19.326, 250.0, 53683.444, 39952.444, 30175.989, 272083.879, 21493.992, 1.206, 102.013])

    nvidia_si_no_stress = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    nvidia_si = take_log([0.94, 0.0, 0.0, 1.415, 1.412, 0.0, 0.0, 1.176, 1.596, 0.0, 0.0, 1.642, 1.426, 0.0, 0.0, 1.405, 0.702, 0.0, 0.0, 1.415, 2.168, 0.0, 0.0, 1.623, 5.961, 6.089, 7.119, 6.064, 5.892, 6.332, 0.464, 0.475])
    nvidia_parallel_no_stress = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    nvidia_up = take_log([4429.06, 0.0, 0.0, 4192.857, 3775.842, 0.0, 0.0, 3834.402, 5880.898, 0.0, 0.0, 5308.594, 4211.527, 0.0, 0.0, 4412.081, 5629.739, 0.0, 0.0, 5421.147, 8771.87, 0.0, 0.0, 8925.991, 274083.03, 280629.653, 161385.723, 164941.252, 559958.307, 566729.968, 2300.879, 2219.738])
    nvidia_sp = take_log([2345.927, 0.0, 0.0, 2010.538, 2358.292, 0.0, 0.0, 2315.758, 2853.575, 0.0, 0.0, 2762.314, 2258.531, 0.0, 0.0, 2259.238, 2507.42, 0.0, 0.0, 2521.802, 3829.727, 0.0, 0.0, 3494.777, 186400.841, 187160.377, 110293.915, 116226.723, 437666.667, 460692.154, 1727.714, 1528.58])

    m1_si_no_stress = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    m1_si = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 14.397, 13.847, 58.883, 59.963, 60.425, 58.727, 0.0, 0.0])
    m1_parallel_no_stress = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    m1_up = take_log([201.19, 0.0, 0.399, 205.28, 216.685, 0.0, 0.0, 185.54, 202.593, 0.324, 0.0, 218.341, 203.482, 0.0, 0.0, 200.975, 231.355, 0.0, 0.0, 258.842, 247.215, 0.541, 0.605, 242.619, 7919.699, 7948.896, 8507.024, 8635.609, 9911.99, 9545.113, 15.066, 11.55])
    m1_sp = take_log([230.143, 0.0, 0.427, 241.053, 244.983, 0.0, 0.0, 230.876, 237.509, 0.695, 0.454, 230.718, 220.08, 0.0, 0.0, 208.417, 277.307, 0.0, 0.562, 274.093, 256.502, 1.225, 0.557, 223.868, 8118.886, 8343.685, 8011.44, 7963.914, 8588.4, 8357.481, 10.847, 11.432])
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(16, 8), constrained_layout=True)
    max_rate_for_device("Intel", ax1, intel_si_no_stress, intel_si, intel_parallel_no_stress, intel_up, intel_sp)
    max_rate_for_device("AMD", ax2, amd_si_no_stress, amd_si, amd_parallel_no_stress, amd_up, amd_sp)
    max_rate_for_device("Nvidia", ax3, nvidia_si_no_stress, nvidia_si, nvidia_parallel_no_stress, nvidia_up, nvidia_sp)
    max_rate_for_device("M1", ax4, m1_si_no_stress, m1_si, m1_parallel_no_stress, m1_up, m1_sp, True)
    handles, labels = ax4.get_legend_handles_labels()
    fig.legend(handles, labels)
    #fig.tight_layout()
    fig.supylabel("Weak behaviors per second (log scale)")
    #fig.suptitle("99.999% Reproducibility Per Device")
    plt.savefig('maxed_rates_per_test.png')
    #plt.show()


def reproducibility():
    labels = [95, 98, 99, 99.9, 99.99, 99.999]
    parallel_no_stress = [19, 19, 18, 18, 17, 17]
    parallel_log_rate = [17, 17, 17, 17, 17, 17]
    parallel_ceiling_log_rate = [19, 19, 19, 19, 19, 19]
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars
    ax.bar(x - width, parallel_no_stress, width, label='Parallel Baseline (No Stress)')
    ax.bar(x, parallel_log_rate, width, label='Parallel, Log Rate Combination')
    ax.bar(x + width, parallel_ceiling_log_rate, width, label='Parallel, Ceiling Log Rate Combination')
    ax.set_xticks(x, labels)
    ax.set_xlabel("Reproducibility Threshold")
    ax.set_ylabel("Number of Tests")
    ax.set_ylim([0, 32])

    fig.legend()
    plt.savefig("figure2.pdf")

def per_test_vs_global():
    labels = [95, 98, 99, 99.9, 99.99, 99.999]
    parallel_unsmoothed_ceiling_log_rate = [19, 19, 19, 19, 19, 19]
    parallel_smoothed_ceiling_log_rate = [20, 19, 19, 19, 19, 19]
    parallel_unsmoothed_global_log_rate = [17, 17, 17, 17, 16, 16]
    parallel_smoothed_global_log_rate = [19, 19, 19, 18, 18, 18]
    parallel_unsmoothed_global_ceiling = [19, 19, 19, 19, 18, 18]
    parallel_smoothed_global_ceiling = [19, 19, 19, 19, 18, 18]
    fig, ax = plt.subplots(1, 1, figsize=(12, 6), constrained_layout=True)
    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars
    ax.bar(x - 2.5 * width, parallel_unsmoothed_ceiling_log_rate, width, label='Unsmoothed Ceiling Log Rate Per Test')
    ax.bar(x - 1.5 * width, parallel_smoothed_ceiling_log_rate, width, label='Smoothed Ceiling Log Rate Per Test')
    ax.bar(x - .5 * width, parallel_unsmoothed_global_log_rate, width, label='Unsmoothed Global Log Rate')
    ax.bar(x + .5 * width, parallel_smoothed_global_log_rate, width, label='Smoothed Global Log Rate')
    ax.bar(x + 1.5 * width, parallel_unsmoothed_global_ceiling, width, label='Unsmoothed Global Ceiling')
    ax.bar(x + 2.5 * width, parallel_smoothed_global_ceiling, width, label='Smoothed Global Ceiling')
    ax.set_xticks(x, labels)
    ax.set_xlabel("Reproducibility Threshold")
    ax.set_ylabel("Number of Tests")
    ax.set_ylim([0, 32])
    fig.legend()
    plt.savefig("figure3.pdf")

def per_test_vs_global_total():
    labels = [95, 98, 99, 99.9, 99.99, 99.999]
    parallel_unsmoothed_ceiling_log_rate = [89, 89, 89, 89, 88, 88]
    parallel_smoothed_ceiling_log_rate = [91, 88, 88, 87, 86, 87]
    parallel_unsmoothed_global_log_rate = [83, 83, 83, 83, 82, 82]
    parallel_smoothed_global_log_rate = [86, 86, 86, 84, 83, 82]
    parallel_unsmoothed_global_ceiling = [88, 87, 87, 85, 84, 84]
    parallel_smoothed_global_ceiling = [88, 88, 88, 86, 85, 85]
    fig, ax = plt.subplots(1, 1, figsize=(12, 6), constrained_layout=True)
    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars
    ax.bar(x - 2.5 * width, parallel_unsmoothed_ceiling_log_rate, width, label='Unsmoothed Ceiling Log Rate Per Test')
    ax.bar(x - 1.5 * width, parallel_smoothed_ceiling_log_rate, width, label='Smoothed Ceiling Log Rate Per Test')
    ax.bar(x - .5 * width, parallel_unsmoothed_global_log_rate, width, label='Unsmoothed Global Log Rate')
    ax.bar(x + .5 * width, parallel_smoothed_global_log_rate, width, label='Smoothed Global Log Rate')
    ax.bar(x + 1.5 * width, parallel_unsmoothed_global_ceiling, width, label='Unsmoothed Global Ceiling')
    ax.bar(x + 2.5 * width, parallel_smoothed_global_ceiling, width, label='Smoothed Global Ceiling')
    ax.set_xticks(x, labels)
    ax.set_xlabel("Reproducibility Threshold")
    ax.set_ylabel("Number of Tests")
    ax.set_ylim([0, 128])
    fig.legend()
    plt.savefig("figure3a.pdf")


def time_budget():
    labels = [95, 98, 99, 99.9, 99.99, 99.999]
    smoothed_half_second = [17, 16, 15, 15, 11, 10]
    smoothed_one_second = [18, 18, 18, 17, 15, 15]
    smoothed_three_seconds = [19, 19, 19, 19, 18, 18]
    smoothed_five_seconds = [19, 19, 19, 19, 19, 19]
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars
    ax.bar(x - 1.5 * width, smoothed_half_second, width, label='Half Second Time Budget')
    ax.bar(x - .5 * width, smoothed_one_second, width, label='One Second Time Budget')
    ax.bar(x + .5 * width, smoothed_three_seconds, width, label='Three Seconds Time Budget')
    ax.bar(x + 1.5 * width, smoothed_five_seconds, width, label='Five Seconds Time Budget')
    ax.set_xticks(x, labels)
    ax.set_xlabel("Reproducibility Threshold")
    ax.set_ylabel("Number of Tests")
    ax.set_ylim([0, 32])
    ax.set_title("Global Combination")
    fig.legend()
    plt.savefig("figure4.pdf")

def time_budget_unsmoothed():
    labels = [95, 98, 99, 99.9, 99.99, 99.999]
    smoothed_half_second = [18, 16, 16, 16, 15, 15]
    smoothed_one_second = [18, 18, 18, 17, 16, 16]
    smoothed_three_seconds = [19, 19, 19, 19, 18, 18]
    smoothed_five_seconds = [19, 19, 19, 19, 19, 18]
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars
    ax.bar(x - 1.5 * width, smoothed_half_second, width, label='Half Second Time Budget')
    ax.bar(x - .5 * width, smoothed_one_second, width, label='One Second Time Budget')
    ax.bar(x + .5 * width, smoothed_three_seconds, width, label='Three Seconds Time Budget')
    ax.bar(x + 1.5 * width, smoothed_five_seconds, width, label='Five Seconds Time Budget')
    ax.set_xticks(x, labels)
    ax.set_xlabel("Reproducibility Threshold")
    ax.set_ylabel("Number of Tests")
    ax.set_ylim([0, 32])
    ax.set_title("Global Combination")
    fig.legend()
    plt.savefig("figure4a.pdf")



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

def take_log(data):
    return [math.log(v + 1, 10) for v in data]

def scatter():
    intel_parallel = take_log([36.06, 0.0, 0.207, 69.324, 40.29, 0.0, 0.0, 40.335, 38.023, 0.0, 0.0, 81.21, 33.333, 0.0, 0.0, 37.093, 80.351, 0.0, 0.0, 219.323, 53.897, 0.0, 0.0, 41.975, 13917.836, 46265.756, 15033.605, 14761.15, 38355.324, 39630.807, 2200.244, 6553.521])
    intel_legacy = take_log([20.518, 0, 2.652, 4.262, 18.589, 0, 0.261, 1.113, 13.808, 0.266, 1.755, 2.697, 1.242, 0, 0, 13.807, 13.493, 0, 0.286, 4.14, 14.022, 0.254, 0.506, 2.271, 120.753, 101.63, 45.7, 54.111, 67.841, 81.467, 0.901, 0.302])

    nvidia_parallel = take_log([4429.06, 0.0, 0.0, 4192.857, 3775.842, 0.0, 0.0, 3834.402, 5880.898, 0.0, 0.0, 5308.594, 4211.527, 0.0, 0.0, 4412.081, 5629.739, 0.0, 0.0, 5421.147, 8771.87, 0.0, 0.0, 8925.991, 274083.03, 280629.653, 161385.723, 164941.252, 559958.307, 566729.968, 2300.879, 2219.738])
    nvidia_legacy = take_log([0.94, 0.0, 0.0, 1.415, 1.412, 0.0, 0.0, 1.176, 1.596, 0.0, 0.0, 1.642, 1.426, 0.0, 0.0, 1.405, 0.702, 0.0, 0.0, 1.415, 2.168, 0.0, 0.0, 1.623, 5.961, 6.089, 7.119, 6.064, 5.892, 6.332, 0.464, 0.475])

    m1_parallel = take_log([201.19, 0.0, 0.399, 205.28, 216.685, 0.0, 0.0, 185.54, 202.593, 0.324, 0.0, 218.341, 203.482, 0.0, 0.0, 200.975, 231.355, 0.0, 0.0, 258.842, 247.215, 0.541, 0.605, 242.619, 7919.699, 7948.896, 8507.024, 8635.609, 9911.99, 9545.113, 15.066, 11.55])
    m1_legacy = take_log([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 14.397, 13.847, 58.883, 59.963, 60.425, 58.727, 0.0, 0.0])

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
    smoothed_min_rates = take_log([20.188, 0.0, 0.0, 27.403, 15.059, 0.0, 0.0, 18.182, 23.14, 0.0, 0.0, 32.779, 16.656, 0.0, 0.0, 12.516, 41.925, 0.0, 0.0, 108.451, 8.748, 0.0, 0.0, 9.434, 250.0, 8343.685, 7973.865, 7963.914, 8588.4, 8280.906, 0.0, 11.432])
    unsmoothed_min_rates = take_log([36.06, 0.0, 0.0, 69.324, 40.29, 0.0, 0.0, 40.335, 38.023, 0.0, 0.0, 81.21, 33.333, 0.0, 0.0, 37.093, 69.82, 0.0, 0.0, 196.444, 14.151, 0.0, 0.0, 16.125, 92.818, 7948.896, 7080.636, 7241.935, 9911.99, 9229.474, 0.0, 11.55])
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
#reproducible()
#max_rate_per_test()
means()
reproducibility()
per_test_vs_global()
per_test_vs_global_total()
time_budget()
time_budget_unsmoothed()

