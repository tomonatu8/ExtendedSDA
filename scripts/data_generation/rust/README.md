# Mallows Distribution Sampling by Rust

This module implements a Rust-based sampler for Mallows distributions, which is used to generate priorities for daycares in matching markets. The sampling method is based on the following paper:
- N. Mattei and T. Walsh. "PrefLib: A Library of Preference Data." In *Proceedings of the 3rd International Conference on Algorithmic Decision Theory (ADT 2013)*, Lecture Notes in Artificial Intelligence. Springer, 2013. [PrefLib Website](http://preflib.org) | [GitHub Repository](https://github.com/PrefLib/preflib)

## Build Rust Code

To build the Rust code, use [PyO3](https://pyo3.rs/) and [maturin](https://www.maturin.rs/). Follow the steps below:
```bash
maturin build -i python3 --release
maturin develop --release --uv
```

## Results
The Rust implementation achieves significant speedups compared to the Python-based PrefLib library. Below is a summary of the performance comparison (M1 Mac Pro):
```bash
Summary:
==================================================
|  Voters | Alternatives | Python-Preflib (s) | Rust (s) |   Speedup |
|---------|--------------|--------------------|----------|-----------|
|    1000 |           50 |              0.767 |    0.004 |   180.61x |
|    1000 |          100 |              1.933 |    0.011 |   168.26x |
|    1000 |          200 |              5.706 |    0.040 |   142.83x |
|    1000 |          500 |             29.743 |    0.153 |   193.90x |
|    1000 |         1000 |            111.962 |    0.572 |   195.77x |
```