import yfinance as yf
import pandas as pd

def get_returns(tickers, period="5Y"):
    """
    Downloads historical 'Adj Close' prices for a list of tickers
    and calculates the daily percentage returns.
    """
    # Download historical data
    data = yf.download(tickers, period=period, auto_adjust=True)['Close']    
    
    # Calculate daily returns
    returns = data.pct_change().dropna()
    
    return returns