# Visualizing the Memory Wall
This repository generates figures that illustrate the **memory-wall problem** in modern GPUs and accelerators.
It produces both **graphics** (e.g. PDF/PNG) and the corresponding **TikZ/PGFPlots code**, making the figures easy to reuse in papers, slides, and LaTeX documents.
The figures are derived from the CSV dataset located [here](https://github.com/rpelke/memory-wall-problem/tree/main/data).


## Download Artefacts
All figures are automatically built in CI.
The latest generated outputs are available on the [gh-pages](https://github.com/rpelke/memory-wall-problem/tree/gh-pages) branch.


## Background & Motivation
The idea for these visualizations is inspired by the first figure of a very nice paper
called [AI and the Memory Wall](https://ieeexplore.ieee.org/document/10477550) by Gholami et al.
The authors also provide a [repository](https://github.com/amirgholami/ai_and_memory_wall).
However, the raw data underlying the first figure is not publicly available.

The goal of this project is therefore to **reconstruct the figure in a transparent and reproducible way**, based on openly collected and documented data.


## Figures in This Repository

### Figure 1: Peak Compute vs. Memory Bandwidth (Fastest Datatype per GPU)
The first figure shows the historical evolution of **peak compute throughput** versus **memory bandwidth** for GPUs and accelerators, always using the **fastest supported floating-point datatype** (not integer) of each architecture.

- Until the mid-2010s, this was typically FP32
- Later generations introduced FP16, bfloat16, FP8, MXFP4, etc.
- In the 2020s, additional gains come from structured sparsity

The exact datatype used for each chip is documented in [`data/datacenter_chips.csv`](https://github.com/rpelke/memory-wall-problem/blob/main/data/datacenter_chips.csv) under the column `dtype`.
This analysis concentrates on floating-point data types.

<p align="center">
  <img src="https://rpelke.github.io/memory-wall-problem/memory_wall_problem.png">
</p>


### Figure 2: Peak Compute vs. Memory Bandwidth (FP32 Only)
The second figure shows the same axes and scaling,
but restricts the data strictly to FP32 performance.

This view highlights how the memory wall already existed before the introduction of low-precision datatypes and sparsity, and helps disentangle architectural scaling effects from numerical format innovations.

<p align="center">
  <img src="https://rpelke.github.io/memory-wall-problem/memory_wall_problem_fp32.png">
</p>


## Further Remarks
Contributions, corrections, and extensions are very welcome.
