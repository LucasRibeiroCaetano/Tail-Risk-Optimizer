# Tail Risk Optimizer

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Libraries-cvxpy-pandas-yfinance](https://img.shields.io/badge/Libraries-cvxpy%20%7C%20pandas%20%7C%20yfinance-orange)](#)
[![License-CC-BY-NC-4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-Green)](https://creativecommons.org/licenses/by-nc/4.0/)

A Python command-line tool for portfolio optimization that focuses on minimizing "tail risk" instead of traditional volatility. This project calculates the ideal asset allocation to minimize **Conditional Value at Risk (CVaR)**, providing a more robust strategy for protecting against extreme market losses.

## Why Use This Optimizer?

Standard Markowitz portfolio optimization defines "risk" as *volatility* (standard deviation). This treats a +10% gain and a -10% loss as equally "risky."

**Tail Risk (CVaR)** is different. It answers the question: **"If things go badly, what is my average loss?"**

This optimizer finds a portfolio that performs best during the worst market scenarios (e.g., the worst 5% of days), making it a powerful tool for defensive investment strategies and risk management.

### Key Features
* **CVaR Optimization:** Finds the portfolio with the lowest Conditional Value at Risk (Expected Shortfall).
* **`cvxpy` Engine:** Uses `cvxpy` for robust and efficient Linear Programming optimization.
* **Market Data:** Fetches up-to-date historical data using the `yfinance` library.
* **Clean Interface:** A simple command-line tool (CLI) with customizable flags.
* **Visual Dashboard:** Generates a `matplotx` dashboard with two panels to visualize the results.

## Output

The tool prints an optimization summary to the console and then displays a visual dashboard in a single window:

1.  **Backtest Graph:** A line chart comparing the cumulative returns of your `Min-CVaR Portfolio` against a baseline `Equal-Weight (1/N) Portfolio`.
2.  **Allocation Chart:** A pie chart showing the optimal asset allocation, with a clear external legend.

## Installation

1.  Clone the repository (or simply create the files locally):
    ```bash
    git clone https://github.com/LucasRibeiroCaetano/Tail-Risk-Optimizer.git
    cd Tail-Risk-Optimizer
    ```

2.  Install the dependencies from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

The script is run from `main.py` and accepts several optional arguments ("flags") to customize the analysis.

```bash
python main.py [--tickers TICKERS] [--period PERIOD] [--alpha ALPHA]
```

## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

This means you are free to:

- Share: copy and redistribute the material in any medium or format.

- Adapt: remix, transform, and build upon the material.

Under the following terms:

- Attribution: You must give appropriate credit.

**NonCommercial**: You may not use the material for commercial purposes.

For the full license text, see: https://creativecommons.org/licenses/by-nc/4.0/