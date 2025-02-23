import pandas.core.config_init
import os
import time
import json
import hackathon_linc as lh
import pandas as pd
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type

count = 0  # Global variable to count trades
# Initialize API
API_KEY = os.getenv('API_KEY')
lh.init(API_KEY)

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3), retry=retry_if_exception_type(Exception))
def safe_placeholder_strategy():
    """
    Wrapper function to safely execute the placeholder strategy with retry logic.
    If an exception occurs, the function will automatically retry up to 3 times with a 2-second delay.
    """
    return placeholder_strategy()

def placeholder_strategy():
    """
    Placeholder strategy function to demonstrate how to retrieve and compare stock prices.
    The function follows these steps:
    1. Retrieves all available tickers.
    2. For each ticker, fetches the current ask price (current price).
    3. Retrieves historical data for the ticker and calculates the price two days ago (old price).
    4. Compares the old price with the current price and places a buy order if the old price is greater.
    5. A retry mechanism ensures the process is robust, even if errors occur during execution.

    Returns a status message and a count of how many trades were placed.
    """

    global count
    tickers = lh.get_all_tickers()
    if not tickers:
        return {"error": "No tickers found"}

    for ticker in tickers:
        current_price_dict = lh.get_current_price(ticker)
        current_price = current_price_dict['data'][0]['askMedian']
        historical_data = lh.get_historical_data(1, ticker)
        df = pd.DataFrame(historical_data)

        # Convert 'gmtTime' to datetime
        df['gmtTime'] = pd.to_datetime(df['gmtTime'])
        df_old = df.loc[df['gmtTime'].idxmin()]

        # Extract the oldest price
        old_price = df_old['askMedian']

        amount = 1  # Define the amount for buying

        # Swing-inspired, buys if price is down
        if old_price > current_price:
            try:
                order_response = lh.buy(ticker, amount)
                print(f"Placed buy order: {amount} share of {ticker} at {current_price} (old price: {old_price}).")
                count += 1
            except json.JSONDecodeError as e:
                print("JSON decoding error:", e)
                return {"error": "Failed to decode JSON response from API."}
        else:
            print("Old price < current price, no trade made")

    return {"status": "Strategy executed", "count": count}

def sell_all_stocks():
    """
    Function to sell all stocks in the portfolio.
    This function retrieves the current portfolio, cancels any outstanding orders, and then sells all the stocks in the portfolio.
    """
    print("Selling all stocks")
    portfolio = lh.get_portfolio()
    print("Selling all stocks in portfolio: ", portfolio)
    for ticker, quantity in portfolio.items():
        print(f"Selling {quantity} of {ticker}")
        lh.sell(ticker, quantity)
    print("Sold all stocks")
    return

# Trading loop using the safe version with retries
while count < 50:
    try:
        ps = safe_placeholder_strategy()
    except Exception as e:
        print("Persistent error after retries:", e)
        continue  # Optionally, break out or log the issue

    time.sleep(1)

sell_all_stocks()
print("Final Balance: ", lh.get_balance())

