"""
Generate pie chart for distribution of deleted tests by projects [rq2]
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams.update({"font.size": 10})

# Data
deleted_tests = [260, 3316,  869,   660, 2070, 151, 17105]
labels = [
    "gson",
    "commons-math",
    "commons-lang",
    "joda-time",
    "pmd",
    "jfreechart",
    "cts",
]

# Set a custom color palette for a more sophisticated look
colors = sns.color_palette("deep")


fig, ax = plt.subplots(figsize=(8, 6))
# plt.figure(figsize=(8, 6))
# plt.pie(deleted_tests, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})


def func(pct, allvals):
    absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
    return f"{absolute:d}"


plt.pie(
    deleted_tests,
    labels=labels,
    autopct=lambda pct: func(pct, deleted_tests),
    pctdistance=0.75,
    startangle=275,
    colors=colors,
    # textprops={"fontsize": 8},
)

# # Draw a circle in the center to make it look like a donut chart
# centre_circle = plt.Circle((0,0),0.70,fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)

# Set title and legend
# plt.title('Distribution of Deleted Tests for Each Library', fontsize=12)
# plt.legend(labels, loc='upper right', bbox_to_anchor=(1.2, 1))

# Show the plot
# plt.show()
# plt.gcf().subplots_adjust(left=0, bottom=0, top=1, right=1, hspace=0, wspace=0)

# plt.gcf().subplots_adjust(bottom=0.5)
# plt.margins(0,0)
# plt.gca().spines[['right', 'top']].set_visible(False)

OUT_DIR = "../io/rq2/figures/"
plt.savefig(OUT_DIR + "deleted_tests_by_projects00.pdf", dpi=1200,  bbox_inches="tight", pad_inches=0,)
plt.savefig(OUT_DIR + "deleted_tests_by_projects00.png", dpi=1200, bbox_inches="tight", pad_inches=0,)
