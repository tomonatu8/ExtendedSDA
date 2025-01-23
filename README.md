# ExtendedSDA

This repository contains the codebase for the paper titled "Probabilistic Analysis of Stable Matching in Large Markets with Siblings". This includes implementations of **Extended Sorted Deferred Acceptance (ESDA)**, and synthetic data generation using Mallows models implemented in Rust.

## Key Features
- **SC (Sequential Couples Algorithm)** [1]
- **SDA (Sorted Deferred Acceptance Algorithm)** [2]
- **ESDA (Extended Sorted Deferred Acceptance Algorithm)**
- **CP (Constraint Programming)** [3]
- **Synthetic Data Generation**


## Setup

### Prerequisites
- Python 3.10
- [Rye](https://rye.astral.sh/) (Python package manager)
- [uv](https://github.com/astral-sh/uv) (Python package installer, used by Rye)
- [Rust](https://www.rust-lang.org/) (for Mallows model)

### Installation

1. **Install Rye**:
```bash
curl -sSf https://rye.astral.sh/get | bash 
source "$HOME/.rye/env"
rye self update
```
2. Configure Rye to use uv:
uv is a fast Python package installer that Rye can use internally. Enable it with:
```bash
rye config --set-bool behavior.use-uv=true
```
3. Install uv:
If uv is not already installed, you can install it manually:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc 
```
4. Verify uv Installation:
Ensure uv is installed correctly by checking its version:
```bash
uv --version
```
5. Install Python dependencies:
```bash
rye pin 3.10
rye sync
```
6. Build Rust Code (Mallows Model):
```bash
cd scripts/data_generation/rust
maturin build -i python3 --release
maturin develop --release --uv
```

## Usage
### Run Tests
To check whether the codes run correctly:
```bash
rye run pytest -s test/test_SC.py
rye run pytest -s test/test_SDA.py
rye run pytest -s test/test_ESDA.py
rye run pytest -s test/test_CP.py
```

To generate synthetic data for experiments:
```bash
rye run pytest -s test/test_data_generation.py 
```


## References

- [1] F. Kojima, P. A. Pathak, and A. E. Roth. Matching with couples: Stability and incentives in large markets. *The Quarterly Journal of Economics*, 128(4):1585-1632, 2013.

- [2] I. Ashlagi, M. Braverman, and A. Hassidim. Stability in large matching markets with complementarities. *Operation
Research*, 62(4):713-732, 2014.

- [3] Z. Sun, N. Yamada, Y. Takenami, D. Moriwaki, and M. Yokoo. Stable matchings in practice: A constraint programming approach. In *Proceedings of the 38th AAAI Conference on Artificial Intelligence (AAAI 2024)*, pages 22377-22384, 2024.