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
from src.pgfplot import pgfplot


def run_plot(settings: PltSettings) -> None:
    df = pd.read_csv(settings.dc_chips_path, sep=",", header=0, decimal=".", encoding="utf-8")
    df = preprocess_data(df, settings)
    regression_lines = calulate_regression_lines(df, settings)
    plot(df, regression_lines, settings)
    pgfplot(df, regression_lines, settings)


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
        ylim=(5 * 10e-2, 3.5 * 10e3),
        text_offsets=0.1,
        mem_bw_label_type="mem_type"
    )

    configs = [
        replace(
            base,
            output_name="memory_wall_problem_fp32.png",
            raw_data_col=["fp32_peak_compute_Gflops", "mem_bw_GBs"],
            marker=["o", "D"],
            y_col=["norm_fp32_peak_compute_Gflops", "norm_mem_bw_GBs"],
            y_label=["FP32 Peak Compute (GFLOPS)", "Memory Bandwidth (GB/s)"],
            marker_color=["royalblue", "mediumseagreen"],
            title="Development of Peak Compute (only FP32) vs. Memory Bandwidth"
        ),
        replace(
            base,
            output_name="memory_wall_problem.png",
            raw_data_col=["ai_dtype_peak_compute_Gflops", "mem_bw_GBs"],
            marker=["v", "D"],
            y_col=["norm_ai_dtype_peak_compute_Gflops", "norm_mem_bw_GBs"],
            y_label=["Peak Compute (GFLOPS)", "Memory Bandwidth (GB/s)"],
            marker_color=["mediumpurple", "mediumseagreen"],
            title="Development of Peak Compute vs. Memory Bandwidth"
        )
    ]

    for cfg in configs:
        run_plot(cfg)
