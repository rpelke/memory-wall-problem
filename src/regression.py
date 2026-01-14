##############################################################################
# Copyright (C) 2026 Rebecca Pelke                                           #
# All Rights Reserved                                                        #
# This work is licensed under the terms described in the LICENSE file        #
# found in the root directory of this source tree.                           #
##############################################################################
from dataclasses import dataclass
import pandas as pd
import numpy as np

from .settings import *


@dataclass
class RegressionLine:
    """
    Represents a regression line in log10 (y-axis) space.
    Attributes:
        A (float): Coefficient in linear space.
        b (float): Exponent coefficient.
        logA (float): log10 of coefficient A.
        factor_20y (float): Growth factor over 20 years.
        factor_2y (float): Growth factor over 2 years.

    Non log-space equation:
        y = A * 10^{b * (x - 2000)}

    Log-space equation:
        log10(y) = log10(A) + b * (x - 2000)
    """
    logA: float
    b: float

    def __post_init__(self):
        if self.logA is None or self.b is None:
            raise ValueError("logA and b must not be None")

        # Convert back to linear space
        self.A = 10**self.logA

        # Growth factors
        self.factor_20y = 10**(20 * self.b)
        self.factor_2y = 10**(2 * self.b)


def calulate_regression_lines(df: pd.DataFrame, settings: PltSettings) -> dict[str, RegressionLine]:
    """Calculates regression lines for each y-column specified in settings.

    Args:
        df (pd.DataFrame): Input DataFrame containing the data.
        settings (PltSettings): Plotting settings including columns to use.

    Returns:
        dict[str, RegressionLine]: Regression lines for each y-column.
    """
    # Shift date by 2000 for better numerical stability.
    x_col = "date_num_minus2000"
    df[x_col] = df["date_num"] - 2000

    regression_lines = {}

    # Calculate regression lines in log10 space.
    for y_col in settings.y_col:
        # log10(y)
        log10_col_name = f"{y_col}_log10"
        df[log10_col_name] = np.log10(df[y_col])

        # Linear regression in log10 space.
        mask = df[x_col].notna() & df[log10_col_name].notna()
        x = df.loc[mask, x_col].to_numpy(dtype=float)
        y = df.loc[mask, log10_col_name].to_numpy(dtype=float)
        b, logA = np.polyfit(x, y, deg=1)
        regression_lines[y_col] = RegressionLine(logA=logA, b=b)

    return regression_lines
