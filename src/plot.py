##############################################################################
# Copyright (C) 2026 Rebecca Pelke                                           #
# All Rights Reserved                                                        #
# This work is licensed under the terms described in the LICENSE file        #
# found in the root directory of this source tree.                           #
##############################################################################
import matplotlib.pyplot as plt

from .regression import *
from .settings import *


def plot(
    df: pd.DataFrame, regression_lines: dict[str, RegressionLine], settings: PltSettings
) -> None:
    """Create the pyplot figure including regression lines.

    Args:
        df (pd.DataFrame): The preprocessed DataFrame.
        regression_lines (dict[str, RegressionLine]): Dictionary of regression lines keyed by column name.
        settings (PltSettings): Plotting settings.
    """
    plt.figure(figsize=(12, 6))
    plt.rcParams["font.family"] = settings.font_family

    for y_col, y_label, marker, marker_color in zip(
        settings.y_col, settings.y_label, settings.marker, settings.marker_color
    ):
        mask = df[y_col].notna() & df["date_num"].notna()
        x = df.loc[mask, "date_pd"],
        y = df.loc[mask, y_col]
        plt.scatter(
            x,
            y,
            label=y_label,
            marker=marker,
            facecolors="none",
            edgecolors=marker_color,
        )

    for (y_col, reg_line), marker_color in zip(regression_lines.items(), settings.marker_color):
        A = reg_line.A
        b = reg_line.b
        y_model = A * 10**(b * (df['date_num'] - 2000))
        label = fr"{int(reg_line.factor_20y):d}$\times$/20 years ({reg_line.factor_2y:.1f}$\times$/2 years)"
        plt.plot(
            df["date_pd"],
            y_model,
            linestyle="--",
            linewidth=settings.regression_line_width,
            color=marker_color,
            label=label
        )

    plt.xlabel("Year", fontsize=settings.label_fontsize)
    plt.ylabel("Normalized Scaling", fontsize=settings.label_fontsize)
    plt.tick_params(axis="both", which="major", labelsize=settings.tick_fontsize)
    plt.title("Development of Peak Compute vs. Memory Bandwidth", fontsize=settings.title_fontsize)
    plt.legend(fontsize=settings.legend_fontsize)
    plt.yscale("log", base=10)
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("memory_wall_problem.png")
    plt.close()
