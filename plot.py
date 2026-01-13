import pandas as pd
import matplotlib.pyplot as plt

# Path to the data center chips CSV file.
DC_CHIPS_PATH = "data/datacenter_chips.csv"

# These columns will be normalized to their first value befor plotting.
NORM_COLS = [
    "mem_bw_GBs",
    "fp32_peak_compute_Gflops",
    "ai_dtype_peak_compute_Gflops",
]

# DataFrame columns to plot on the y-axis.
Y_COLS = ["norm_mem_bw_GBs", "norm_fp32_peak_compute_Gflops", "norm_ai_dtype_peak_compute_Gflops"]

# Y-labels for the plots.
Y_LABELS = [
    "Normalized Memory Bandwidth (GB/s)", "Normalized FP32 Peak Compute (GFLOPS)",
    "Normalized Peak Compute (GFLOPS)"
]

df = pd.read_csv(DC_CHIPS_PATH, sep=";", header=0, decimal=".", encoding="utf-8")


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
    df = sort_by_date(df)
    df["date_pd"] = pd.to_datetime(df["date_de"], format="%d.%m.%Y")
    normalize_columns(df, NORM_COLS)
    return df


# Plots the normalized values over time.
def plot(df):
    plt.figure(figsize=(12, 6))

    for y_col, y_label in zip(Y_COLS, Y_LABELS):
        mask = df[y_col].notna() & df["date_num"].notna()
        x = df.loc[mask, "date_pd"],
        y = df.loc[mask, y_col]
        plt.scatter(x, y, label=y_label)

    plt.xlabel("Year")
    plt.ylabel("Normalized value")
    plt.title("Development of Peak Compute vs. Memory Bandwidth")
    plt.legend()
    plt.yscale("log")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("memory_wall_problem.png")
    plt.close()


df = preprocess_date(df)
plot(df)
