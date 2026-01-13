##############################################################################
# Copyright (C) 2026 Rebecca Pelke                                           #
# All Rights Reserved                                                        #
# This work is licensed under the terms described in the LICENSE file        #
# found in the root directory of this source tree.                           #
##############################################################################
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PltSettings:
    """Contains all information for one pyplot figure.
    Attributes:
        dc_chips_path (Path): Path to the data file.
        output_name (str): Name of the output plot file.
        raw_data_col (list[str]): Columns to normalize.
        y_col (list[str]): Columns to plot on y-axis.
        y_label (list[str]): Labels for y-axis columns.
        marker (list[str]): Markers for each y-column.
        marker_color (list[str]): Colors for each marker.
        label_fontsize (int): Font size for axis labels.
        tick_fontsize (int): Font size for tick labels.
        title_fontsize (int): Font size for the plot title.
        legend_fontsize (int): Font size for the legend.
        annotation_fontsize (int): Font size for point annotations.
        font_family (str): Font family for the plot.
        regression_line_width (float): Line width for regression lines.
        text_offsets (float): Offsets for text annotations in percentage.
        title (str): Title of the plot.
    """
    dc_chips_path: Path
    output_name: str
    raw_data_col: list[str]
    y_col: list[str]
    y_label: list[str]
    marker: list[str]
    marker_color: list[str]
    label_fontsize: int = 12
    tick_fontsize: int = 10
    title_fontsize: int = 14
    legend_fontsize: int = 12
    annotation_fontsize: int = 8
    font_family: str = "monospace"
    regression_line_width: float = 1.0
    text_offsets: float = 0.15
    title: str = None

    # Verify that all lists have the same length.
    def __post_init__(self):
        list_fields = {name: value for name, value in vars(self).items() if isinstance(value, list)}
        if not list_fields:
            return
        lengths = {name: len(value) for name, value in list_fields.items()}
        if len(set(lengths.values())) != 1:
            raise ValueError(
                "All list fields must have the same length. "
                f"Got lengths: {lengths}"
            )
