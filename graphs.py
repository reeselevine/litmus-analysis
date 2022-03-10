import matplotlib.pyplot as plt
import numpy as np
import math

def scatter_colors(parallel, legacy):
    colors = []
    for i in range(0, len(parallel)):
        if parallel[i] >= legacy[i]:
            colors.append("limegreen")
        else:
            colors.append("tomato")
    return colors

def scatter():
    parallel = [16.538, 0.0, 0.0, 22.915, 15.799, 0.0, 0.0, 24.606, 16.782, 0.0, 0.0, 37.693, 16.051, 0.0, 0.0, 24.065, 49.117, 0.0, 0.0, 119.312, 25.496, 0.168, 0.0, 29.454, 6437.726, 26038.079, 8639.277, 9033.213, 19637.821, 21373.699, 1182.334, 4637.23]
    legacy = [20.518, 0, 2.652, 4.262, 18.589, 0, 0.261, 1.113, 13.808, 0.266, 1.755, 2.697, 1.242, 0, 0, 13.807, 13.493, 0, 0.286, 4.14, 14.022, 0.254, 0.506, 2.271, 120.753, 101.63, 45.7, 54.111, 67.841, 81.467, 0.901, 0.302]

    parallel = [math.log(v + 1) for v in parallel]
    legacy = [math.log(v + 1) for v in legacy]
    colors = scatter_colors(parallel, legacy)

    plt.scatter(parallel, legacy, c=colors, marker="^")
    #plt.plot([0, 10], [0, 10], color="lightskyblue")
    plt.xlabel("Max unsmoothed parallel instance rate")
    plt.ylabel("Max unsmoothed single instance rate")
    plt.title("Intel Iris")

    plt.show()

def grouped_bar():
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 34, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, men_means, width, label='Men')
    rects2 = ax.bar(x + width/2, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()

scatter()

