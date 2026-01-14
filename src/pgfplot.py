##############################################################################
# Copyright (C) 2026 Nils Bosbach                                            #
# All Rights Reserved                                                        #
# This work is licensed under the terms described in the LICENSE file        #
# found in the root directory of this source tree.                           #
##############################################################################

from .regression import RegressionLine
from .settings import PltSettings
import math
import os
import pandas as pd

marker_dict = {"D": "diamond*", "v": "triangle*", "o": "*"}
regression_dict = {"mediumseagreen": "densely dashed", "royalblue": "densely dotted"}
anchor_dict = {"b": "north", "t": "south"}

label_cols = {"norm_mem_bw_GBs": "mem_type"}


def add_properties(outfile: list, properties: dict, indent: int) -> None:
    for property, value in properties.items():
        outfile.append((indent, f"{property}={value}," if value is not None else f"{property},"))


def pgfplot(
    df: pd.DataFrame, regression_lines: dict[str, RegressionLine], settings: PltSettings
) -> None:
    """Create a pgfplots-based figure including regression lines.

    Args:
        df (pd.DataFrame): The preprocessed DataFrame.
        regression_lines (dict[str, RegressionLine]): Dictionary of regression lines keyed by column name.
        settings (PltSettings): Plotting settings.
    """
    outfile = []
    indent = 0

    outfile.append((indent, r"% \usepackage{tikz}"))
    outfile.append((indent, r"% \usepackage{pgfplots}"))
    outfile.append((indent, r"% \pgfplotsset{compat=1.14}"))
    outfile.append((0, ""))

    outfile.append((indent, r"\begin{figure}"))
    indent += 1

    outfile.append((indent, r"\centering"))
    outfile.append((indent, r"\begin{tikzpicture}"))
    indent += 1

    outfile.append((indent, r"\begin{axis}["))
    indent += 1

    axis_properties = {
        "width":
            "15.4cm",
        "height":
            "7cm",
        "xlabel":
            "{Year}",
        "ylabel":
            "{Normalized Scaling}",
        "ymode":
            "log",
        "log basis y":
            "10",
        "grid":
            "major",
        "minor grid style":
            "dotted",
        "scaled x ticks":
            "false",
        "xticklabel style":
            "{/pgf/number format/fixed, /pgf/number format/precision=0, /pgf/number format/1000 sep={}}",
        "legend pos":
            "north west",
        "legend cell align":
            "left",
        "legend style":
            r"{font=\scriptsize}",
    }
    add_properties(outfile, axis_properties, indent)

    indent -= 1
    outfile.append((indent, r"]"))
    indent += 1

    for raw_data_col, y_col, y_label, marker, marker_color in zip(
        settings.raw_data_col, settings.y_col, settings.y_label, settings.marker,
        settings.marker_color
    ):
        # yapf: disable
        outfile.append((indent, rf"% {'-' * 10} {y_label}"))
        # yapf: enable

        outfile.append((indent, r"\addplot ["))
        indent += 1

        plot_properties = {
            "only marks": None,
            "mark": marker_dict.get(marker, "D"),
            "draw": "none",
            "fill": "gray!75"
        }
        add_properties(outfile, plot_properties, indent)

        indent -= 1
        outfile.append((indent, r"] coordinates {"))
        indent += 1

        for _, row in df.iterrows():
            if pd.isna(row[y_col]):
                continue
            outfile.append((indent, f"({row['date_num']}, {row[y_col]})"))

        indent -= 1
        outfile.append((indent, r"};"))

        outfile.append((indent, rf"\addlegendentry{{{y_label}}}"))
        outfile.append((0, ""))

        if y_col in regression_lines:
            outfile.append((indent, "% Regression line"))
            outfile.append((indent, r"\addplot ["))
            indent += 1

            xmin = math.floor(df["date_num"].min())
            xmax = math.ceil(df["date_num"].max())
            line_type = regression_dict.get(marker_color, "dotted")

            plot_properties = {line_type: None, "domain": f"{xmin}:{xmax}", "samples": 200}
            add_properties(outfile, plot_properties, indent)

            indent -= 1
            outfile.append(
                (
                    indent,
                    rf"] {{ {regression_lines[y_col].A} * 10^({regression_lines[y_col].b} * (x - 2000))}};"
                )
            )
            outfile.append(
                (
                    indent,
                    rf"\addlegendentry{{{regression_lines[y_col].factor_20y:.0f}\,$\times$/20\,yrs ({regression_lines[y_col].factor_2y:.1f}\,$\times$/2\,yrs)}}"
                )
            )
            outfile.append((0, ""))

        outfile.append((indent, "% Data labels"))

        label_col = label_cols.get(y_col, "name")
        for _, row in df.iterrows():
            label_pos_col = f"{raw_data_col}_labels"
            if label_pos_col not in row or pd.isna(row[label_pos_col]) or pd.isna(row[y_col]):
                continue

            outfile.append(
                (
                    indent,
                    rf"\node[anchor={anchor_dict.get(row[label_pos_col], 'south')}, font=\tiny] at (axis cs:{row['date_num']}, {row[y_col]}) {{{row[label_col]}}};"
                )
            )
        outfile.append((0, ""))

    indent -= 1
    outfile.append((indent, r"\end{axis}"))

    indent -= 1
    outfile.append((indent, r"\end{tikzpicture}"))

    outfile.append((0, ""))
    outfile.append((indent, rf"\caption{{{settings.title}}}"))
    outfile.append((indent, rf"\label{{fig:{os.path.splitext(settings.output_name)[0]}}}"))

    indent -= 1
    outfile.append((indent, r"\end{figure}"))

    with open(f"{os.path.splitext(settings.output_name)[0]}.tex", "w") as f:
        f.writelines([f"{i * 4 * ' '}{line}\n" for i, line in outfile])
