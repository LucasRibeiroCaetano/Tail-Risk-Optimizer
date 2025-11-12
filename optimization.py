import cvxpy as cp
import numpy as np

def optimize_cvar(returns, alpha=0.95):
    """
    Performs CVaR optimization on a portfolio of assets.
    
    This optimization is formulated as a Linear Program to find
    the weights that minimize the Conditional Value at Risk (CVaR).
    
    Returns:
        - weights (np.array): The optimal portfolio weights.
        - var (float): The portfolio's optimized Value at Risk (VaR).
        - cvar (float): The portfolio's optimized Conditional Value at Risk (CVaR).
    """
    # Get the number of assets and observations
    n_assets = returns.shape[1]
    n_obs = returns.shape[0]
    
    # Convert returns dataframe to numpy array
    returns_array = returns.values
    
    # --- CVXPY Optimization Problem ---
    
    # Define variables
    w = cp.Variable(n_assets)          # Portfolio weights
    var = cp.Variable()                # Value at Risk (VaR)
    
    # Auxiliary variable for losses exceeding VaR
    # This is (Loss - VaR), and 0 if (Loss - VaR) is negative
    z = cp.Variable(n_obs)
    
    # Portfolio loss for each observation
    # We use -returns to represent loss
    portfolio_loss = -returns_array @ w
    
    # --- Objective Function ---
    # We aim to minimize the CVaR.
    # CVaR = VaR + (1 / (1-alpha)) * (1/n_obs) * sum(z)
    cvar = var + (1.0 / (1.0 - alpha)) * (1.0 / n_obs) * cp.sum(z)
    objective = cp.Minimize(cvar)
    
    # --- Constraints ---
    constraints = [
        cp.sum(w) == 1,       # Weights sum to 1
        w >= 0,               # No short selling
        
        # CVaR constraints
        # z >= (Portfolio Loss - VaR)
        # z >= 0
        z >= 0,
        z >= portfolio_loss - var
    ]
    
    # Solve the problem
    problem = cp.Problem(objective, constraints)
    problem.solve()
    
    # Check if the problem was solved successfully
    if problem.status != 'optimal':
        raise Exception("Optimization failed to find an optimal solution.")
        
    # Get the results
    optimal_weights = w.value
    var_value = var.value
    cvar_value = cvar.value
    
    return optimal_weights, var_value, cvar_value