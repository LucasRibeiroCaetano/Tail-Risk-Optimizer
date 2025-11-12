import argparse
import numpy as np
import data
import optimization
import plots

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Tail Risk Optimizer (CVaR)")
    
    parser.add_argument(
        '--tickers',
        nargs='*',
        default=['SPY', 'GLD', 'IEF', 'QQQ'],
        help="List of asset tickers (e.g., AAPL MSFT)"
    )
    
    parser.add_argument(
        '--period',
        type=str,
        default='5Y',
        help="Historical period for data (e.g., 1Y, 5Y, 10Y, max)"
    )
    
    parser.add_argument(
        '--alpha',
        type=float,
        default=0.95,
        help="Confidence level for VaR/CVaR (e.g., 0.95)"
    )
    return parser.parse_args()

def main():
    """
    Main entry point for the Tail Risk Optimizer.
    Orchestrates data fetching, optimization, and plotting.
    """
    # 1. Get user inputs
    args = parse_args()
    
    print("--- TailRiskOptimizer ---")
    print(f"Running for: {', '.join(args.tickers)}")
    print(f"Period: {args.period}, Confidence: {args.alpha * 100}%")
    print("-------------------------\n")
    
    try:
        # 2. Get returns data
        returns = data.get_returns(args.tickers, args.period)
        
        # 3. Get optimal portfolio
        weights, var, cvar = optimization.optimize_cvar(returns, args.alpha)
        
        # 4. Print console report
        print("--- Optimization Results ---")
        print(f"Optimal VaR ({args.alpha * 100}%): {var * 100:.4f}%")
        print(f"Optimal CVaR ({args.alpha * 100}%): {cvar * 100:.4f}%\n")
        
        print("Optimal Portfolio Weights:")
        for ticker, weight in zip(args.tickers, weights):
            if weight > 0.0001: # Only show non-zero weights
                print(f"  {ticker}: {weight * 100:.2f}%")
        
        # 5. Show plots
        # Calculate the returns of the optimized portfolio for backtesting
        min_cvar_portfolio_returns = (returns * weights).sum(axis=1)
        
        plots.show_plots(args.tickers, weights, returns, min_cvar_portfolio_returns)
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your tickers or try a different period.")

if __name__ == "__main__":
    main()