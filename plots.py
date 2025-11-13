import matplotlib.pyplot as plt
import matplotx
import numpy as np
import pandas as pd

def show_plots(tickers, optimal_weights, returns, min_cvar_portfolio_returns):
    """
    Generates and displays the results in a 2-subplot figure.
    1. Cumulative returns backtest (70% width).
    2. Pie chart of optimal weights (30% width).
    """
    # Set the matplotx theme
    plt.style.use(matplotx.styles.github["dark"])
    
    # --- Create the plots ---
    
    # 1 row, 2 columns. 70/30 width split.
    # We also make the figure wider (figsize)
    fig, (ax1, ax2) = plt.subplots(
        1, 2,  # 1 row, 2 columns
        figsize=(18, 8), # Wider figure
        gridspec_kw={'width_ratios': [0.7, 0.3]} # 70% / 30% split
    )
    
    # --- Título Principal da Figura (opcional) ---
    fig.suptitle("Análise do Otimizador de Risco (CVaR)", fontsize=16)

    
    # --- Subplot 1 (70%): Cumulative Returns (Backtest) ---
    # This code was previously on ax2
    ax1.set_title("Backtest: CVaR Portfolio vs. Equal-Weight")
    
    # (Cálculo do Equal-Weight)
    n_assets = len(tickers)
    equal_weights = np.array([1/n_assets] * n_assets)
    equal_weight_returns = (returns * equal_weights).sum(axis=1)

    ax1.plot((1 + min_cvar_portfolio_returns).cumprod(), label="Min-CVaR Portfolio")
    ax1.plot((1 + equal_weight_returns).cumprod(), label="Equal-Weight (1/N) Portfolio")
    
    ax1.set_ylabel("Cumulative Growth (1.0 = start)")
    ax1.set_xlabel("Date")
    ax1.legend()

    
    # --- Subplot 2 (30%): Optimal Portfolio Weights (Pie Chart) ---
    # This code was previously on ax1
    ax2.set_title("Optimal CVaR Portfolio Weights")
    
    weights_series = pd.Series(optimal_weights, index=tickers)
    positive_weights_mask = weights_series > 1e-4 
    filtered_weights = weights_series[positive_weights_mask]
    filtered_tickers = filtered_weights.index.tolist()
    filtered_weights_values = filtered_weights.values

    ax2.pie(filtered_weights_values, labels=None, startangle=90)
    
    legend_labels = [f"{ticker}: {weight*100:.2f}%" 
                     for ticker, weight in zip(filtered_tickers, filtered_weights_values)]
    
    # Adjust legend position
    ax2.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))

    
    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.92]) # Ajusta para dar espaço ao suptitle
    plt.show()