import matplotlib.pyplot as plt
import matplotx
import numpy as np
import pandas as pd

def show_plots(tickers, optimal_weights, returns, min_cvar_portfolio_returns):
    """
    Generates and displays the results in a 2-subplot figure.
    1. Pie chart of optimal weights.
    2. Cumulative returns backtest.
    """
    # Set the matplotx theme
    plt.style.use(matplotx.styles.github["dark"])
    
    # --- Calculate data for plots ---
    
    # 1. Equal-Weight (1/N) Portfolio Returns
    n_assets = len(tickers)
    equal_weights = np.array([1/n_assets] * n_assets)
    equal_weight_returns = (returns * equal_weights).sum(axis=1)
    
    # 2. Cumulative Returns
    cum_cvar_returns = (1 + min_cvar_portfolio_returns).cumprod()
    cum_equal_weight_returns = (1 + equal_weight_returns).cumprod()

    # --- Create the plots ---
    
    # Create a single figure with two subplots (2 rows, 1 column)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    
    # --- Subplot 1: Optimal Portfolio Weights (Pie Chart) ---
    ax1.set_title("Optimal CVaR Portfolio Weights")
    
    # Filter out extremely small weights for plotting stability and clearer legends
    # We should ensure that if a weight is non-zero, it's included, 
    # but the legend labels should accurately reflect what's plotted.
    
    # Create a pandas Series from weights and tickers for easy filtering and sorting
    weights_series = pd.Series(optimal_weights, index=tickers)
    
    # Filter for weights greater than a very small threshold (e.g., 0.1%)
    # This prevents plotting invisible tiny slices that still show up in the legend
    # However, for 11.84%, it should definitely be included, so the issue might be ordering.
    # Let's ensure non-zero weights are handled.
    
    # Filter out weights that are effectively zero (due to optimization solver precision)
    positive_weights_mask = weights_series > 1e-4 # Threshold, e.g., 0.01%
    filtered_weights = weights_series[positive_weights_mask]
    filtered_tickers = filtered_weights.index.tolist()
    filtered_weights_values = filtered_weights.values

    # Plot the pie chart without labels on the wedges
    # Ensure the weights passed to pie() correspond directly to the filtered_tickers
    ax1.pie(filtered_weights_values, labels=None, startangle=90)
    
    # Create a separate legend using the filtered tickers and their weights
    # Format labels to show percentage
    legend_labels = [f"{ticker}: {weight*100:.2f}%" 
                     for ticker, weight in zip(filtered_tickers, filtered_weights_values)]
    
    ax1.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))

    
    # --- Subplot 2: Cumulative Returns (Backtest) ---
    ax2.set_title("Backtest: CVaR Portfolio vs. Equal-Weight")
    
    ax2.plot(cum_cvar_returns, label="Min-CVaR Portfolio")
    ax2.plot(cum_equal_weight_returns, label="Equal-Weight (1/N) Portfolio")
    
    # Format the y-axis as a multiplier (e.g., 1.5x)
    ax2.set_ylabel("Cumulative Growth (1.0 = start)")
    ax2.set_xlabel("Date")
    ax2.legend()
    
    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()