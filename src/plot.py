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
    plt.figure(figsize=(12, 8))
    plt.rcParams["font.family"] = settings.font_family

    for d_col, y_col, y_label, marker, marker_color in zip(
        settings.raw_data_col, settings.y_col, settings.y_label, settings.marker,
        settings.marker_color
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

        def _plot_point_labels():
            """Plot optional point labels if available in the DataFrame."""
            label_col = f"{d_col}_labels"

            if label_col in df.columns:
                label_pos = df.loc[mask, label_col]
                label_name = df.loc[mask, "name"]
                l_x = df.loc[mask, "date_pd"]
                l_y = df.loc[mask, y_col]

                for xi, yi, l_pos, l_name in zip(l_x, l_y, label_pos, label_name):
                    if pd.isna(l_pos):
                        continue

                    yi_text = yi * (1 + settings.text_offsets
                                   ) if l_pos == "t" else yi * (1 - settings.text_offsets)
                    plt.annotate(
                        l_name, (xi, yi),
                        xytext=(xi, yi_text),
                        textcoords="data",
                        ha="center",
                        va="bottom" if l_pos == "t" else "top",
                        fontsize=settings.annotation_fontsize,
                        color=marker_color,
                        bbox=dict(
                            boxstyle="round,pad=0.05",
                            facecolor="white",
                            edgecolor="black",
                            linewidth=0.3,
                            alpha=1.0,
                        )
                    )

        _plot_point_labels()

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
    if settings.title != None:
        plt.title(settings.title, fontsize=settings.title_fontsize)
    plt.legend(fontsize=settings.legend_fontsize, loc="upper left")
    plt.yscale("log", base=10)
    if settings.ylim is not None:
        plt.ylim(*settings.ylim)
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(settings.output_name)
    plt.close()
