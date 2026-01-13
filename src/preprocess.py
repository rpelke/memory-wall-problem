##############################################################################
# Copyright (C) 2026 Rebecca Pelke                                           #
# All Rights Reserved                                                        #
# This work is licensed under the terms described in the LICENSE file        #
# found in the root directory of this source tree.                           #
##############################################################################
from .settings import PltSettings
import pandas as pd


def preprocess_data(df: pd.DataFrame, settings: PltSettings) -> pd.DataFrame:
    assert len(settings.raw_data_col) == len(settings.y_col) == len(settings.y_label
                                                                   ) == len(settings.marker)
    """Preprocesses the original dataframe.
    Sorts columns by date.
    Normalizes columns to their first data point.

    Returns:
        df (pd.DataFrame): Preprocessed DataFrame.
    """
    def _sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
        """Sorts the DataFrame by the 'date_num' column in ascending order."""
        return df.sort_values(by="date_num", ascending=True)

    def _normalize_columns(df: pd.DataFrame, columns: list[str]) -> None:
        """Normalizes specified columns to their first value.
        Adds new columns with 'norm_' prefix.

        Args:
            df (pd.DataFrame): Input DataFrame.
            columns (list[str]): List of column names to normalize.
        """
        for c in columns:
            first_val = df[c].iloc[0]
            df[f"norm_{c}"] = df[c] / first_val

    df = _sort_by_date(df)
    df["date_pd"] = pd.to_datetime(df["date_de"], format="%d.%m.%Y")
    _normalize_columns(df, settings.raw_data_col)
    return df
