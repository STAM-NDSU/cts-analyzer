import os.path
from pathlib import Path
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn
import numpy as np
import sys

from pmd import data as pmd
from commons_lang import data as commons_lang
from commons_math import data as commons_math
from cts import data as cts
from jfreechart import data as jfreechart
from gson import data as gson
from joda_time import data as joda_time

# Redirect console ouput to a file
sys.stdout = open("./calc_stdout.txt", "w")

projects_map = {
    "commons-lang": commons_lang,
    "gson": gson,
    "commons-math": commons_math,
    "joda-time": joda_time,
    "jfreechart": jfreechart,
    "pmd": pmd,
    "cts": cts,
}

results = []
for project, data in projects_map.items():
    print(project)
    total_deleted_percent = list(
        map(
            lambda each: round(100 * each["Total Deleted"] / each["Total tests"], 2),
            data.values(),
        )
    )
    print("Total test deletion commit : " + str(len(total_deleted_percent)))

    # total_deleted_percent = list(map(lambda each : each["Total Deleted %"], results))
    print("Mean: ", np.mean(total_deleted_percent))
    print("Median: ", np.median(total_deleted_percent))
    print("Q1: ", np.percentile(total_deleted_percent, 25))
    print("Q3: ", np.percentile(total_deleted_percent, 75))
    print("Max: ", np.max(total_deleted_percent))
    print("Min: ", np.min(total_deleted_percent))
    print("-------------xxxxxxxxxx------------")
