import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class PlotSettings:
    dc_chips_path: Path
    norm_col: list[str]
    y_col: list[str]
    y_label: list[str]
    marker: list[str]
    marker_color: list[str]
    label_fontsize: int = 12
    tick_fontsize: int = 10
    title_fontsize: int = 14
    legend_fontsize: int = 12
    font_family: str = "monospace"

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


# Sorts DataFrame by 'date_num' column in ascending order.
def sort_by_date(df):
    return df.sort_values(by="date_num", ascending=True)


# Normalizes specified columns to their first value.
# Adds new columns with 'norm_' prefix.
def normalize_columns(df, columns):
    for c in columns:
        first_val = df[c].iloc[0]
        df[f"norm_{c}"] = df[c] / first_val


# Preprocesses the DataFrame.
def preprocess_date(df):
    assert len(settings.norm_col) == len(settings.y_col) == len(settings.y_label
                                                               ) == len(settings.marker)
    df = sort_by_date(df)
    df["date_pd"] = pd.to_datetime(df["date_de"], format="%d.%m.%Y")
    normalize_columns(df, settings.norm_col)
    return df


# Plots the normalized values over time.
def plot(df):
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

    plt.xlabel("Year", fontsize=settings.label_fontsize)
    plt.ylabel("Normalized value", fontsize=settings.label_fontsize)
    plt.tick_params(axis="both", which="major", labelsize=settings.tick_fontsize)
    plt.title("Development of Peak Compute vs. Memory Bandwidth", fontsize=settings.title_fontsize)
    plt.legend(fontsize=settings.legend_fontsize)
    plt.yscale("log")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("memory_wall_problem.png")
    plt.close()


if __name__ == '__main__':
    settings = PlotSettings(
        dc_chips_path=Path("data/datacenter_chips.csv"),
        norm_col=[
            "mem_bw_GBs",
            "fp32_peak_compute_Gflops",
            "ai_dtype_peak_compute_Gflops",
        ],
        marker=["D", "o", "v"],
        y_col=[
            "norm_mem_bw_GBs",
            "norm_fp32_peak_compute_Gflops",
            "norm_ai_dtype_peak_compute_Gflops",
        ],
        y_label=[
            "Normalized Memory Bandwidth (GB/s)",
            "Normalized FP32 Peak Compute (GFLOPS)",
            "Normalized Peak Compute (GFLOPS)",
        ],
        marker_color=["firebrick", "royalblue", "mediumseagreen"],
        label_fontsize=14,
        tick_fontsize=12,
        title_fontsize=14,
        legend_fontsize=14
    )

    df = pd.read_csv(settings.dc_chips_path, sep=";", header=0, decimal=".", encoding="utf-8")

    df = preprocess_date(df)
    plot(df)
