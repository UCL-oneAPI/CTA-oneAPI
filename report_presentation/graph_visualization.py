from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def visualization_overall(warnings, image_path):
    warning_codes = []
    file_codes = {}
    files_contain_warnings = {}
    for i in warnings:
        warning_codes.append(i.warning_code)
        file_codes.setdefault(i.warning_code, []).append(i.file_path)
    occurrence = Counter(warning_codes)

    for k, v in file_codes.items():
        files_contain_warnings[k] = len(list(set(v)))

    x = np.arange(len(occurrence.keys()))
    bar_width = 0.2
    plt.figure(num=2, figsize=(20,12))
    plt.bar(x, occurrence.values(), bar_width, align="center", color="green", label="Number of Occurrences", alpha=0.5)
    plt.bar(x + bar_width, files_contain_warnings.values(), bar_width, align="center", color="blue",
            label="Number of documents containing such warnings",
            alpha=0.5)
    plt.xticks(x + bar_width / 2, occurrence.keys())
    max_warnings = max(occurrence.values()) if occurrence.values() else 0
    plt.yticks(np.arange(0, max_warnings + 1, step=5))
    plt.ylabel("Occurrence")
    plt.title("Warning Types with Number of Occurrences (Overall)")
    plt.legend(loc="upper left", fontsize="x-small")
    plt.savefig(str(image_path) + '/before-overall.png')
    plt.close()


def visualization_partial(warnings, image_path):
    file_warnings = {}
    codes = set()
    for i in warnings:
        file_name = Path(i.file_path).name
        file_warnings.setdefault(file_name, []).append(i.warning_code)
        codes.add(i.warning_code)
    for k, v in file_warnings.items():
        warning_distribution = Counter(v)
        for code in codes:
            if code not in warning_distribution.keys():
                warning_distribution[code] = 0
        x = np.arange(len(codes))
        bar_width = 0.2
        plt.bar(x, warning_distribution.values(), bar_width, align="center", color='blue', alpha=0.5)
        plt.xticks(x, warning_distribution.keys())
        max_value = max(warning_distribution.values()) + 1
        if max_value <= 10:
            step = 1
        else:
            step = 3
        plt.yticks(np.arange(0, max_value, step=step))
        plt.ylabel("Occurrence")
        plt.title("Warnings in " + k)
        plt.savefig(str(image_path) + '/' + k + '.jpg')
        plt.close()
