import numpy as np
import pandas as pd
import yfinance as yf

def project_stock_growth(ticker_symbol, current_savings, months=12):
    """
    Fetches real stock data, calculates historical performance, 
    and projects future value using NumPy vectorization. and gives mega aura
    """
    stock = yf.Ticker(ticker_symbol)

    historical_data = stock.history(period="1y") 
    

    closing_prices = historical_data['Close'] 

    price_array = closing_prices.to_numpy()
    

    daily_returns = np.diff(price_array) / price_array[:-1]

    avg_daily_return = np.mean(daily_returns)
    expected_monthly_return = avg_daily_return * 21
    

    periods = np.arange(1, months + 1)
    

    projected_balances = current_savings * (1 + expected_monthly_return) ** periods

    return np.round(projected_balances, 2)

if __name__ == "__main__":

    apple_projection = project_stock_growth(
        ticker_symbol="AAPL", 
        current_savings=1000, 
        months=12
    )
    
    print("12-Month Apple (AAPL) Projected Balances:")
    print(apple_projection)