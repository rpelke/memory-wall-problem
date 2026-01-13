##############################################################################
# Copyright (C) 2026 Rebecca Pelke                                           #
# All Rights Reserved                                                        #
# This work is licensed under the terms described in the LICENSE file        #
# found in the root directory of this source tree.                           #
##############################################################################
import pandas as pd
from pathlib import Path
from dataclasses import replace

from src.regression import *
from src.settings import *
from src.preprocess import *
from src.plot import plot


def run_plot(settings: PltSettings) -> None:
    df = pd.read_csv(settings.dc_chips_path, sep=",", header=0, decimal=".", encoding="utf-8")
    df = preprocess_data(df, settings)
    regression_lines = calulate_regression_lines(df, settings)
    plot(df, regression_lines, settings)


if __name__ == "__main__":
    base = PltSettings(
        dc_chips_path=Path("data/datacenter_chips.csv"),
        output_name="memory_wall_problem.png",
        raw_data_col=[],
        marker=[],
        y_col=[],
        y_label=[],
        marker_color=[],
        label_fontsize=14,
        tick_fontsize=12,
        title_fontsize=14,
        legend_fontsize=14,
        annotation_fontsize=10,
        text_offsets=0.1
    )

    configs = [
        replace(
            base,
            output_name="memory_wall_problem_fp32.png",
            raw_data_col=["mem_bw_GBs", "fp32_peak_compute_Gflops"],
            marker=["D", "o"],
            y_col=["norm_mem_bw_GBs", "norm_fp32_peak_compute_Gflops"],
            y_label=["Memory Bandwidth (GB/s)", "FP32 Peak Compute (GFLOPS)"],
            marker_color=["firebrick", "royalblue"],
            title="Development of Peak Compute (only FP32) vs. Memory Bandwidth"
        ),
        replace(
            base,
            output_name="memory_wall_problem.png",
            raw_data_col=["mem_bw_GBs", "ai_dtype_peak_compute_Gflops"],
            marker=["D", "v"],
            y_col=["norm_mem_bw_GBs", "norm_ai_dtype_peak_compute_Gflops"],
            y_label=["Memory Bandwidth (GB/s)", "Peak Compute (GFLOPS)"],
            marker_color=["firebrick", "mediumseagreen"],
            title="Development of Peak Compute vs. Memory Bandwidth"
        ),
    ]

    for cfg in configs:
        run_plot(cfg)
