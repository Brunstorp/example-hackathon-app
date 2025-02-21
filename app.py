from flask import Flask, render_template_string
import hackathon_linc as lh
import pandas as pd
import random
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Initialize the API with your API key
lh.init(API_KEY)

def get_portfolio_df():
    """
    Retrieves portfolio as a pandas DataFrame.
    Assumes lh.get_portfolio() returns a dictionary mapping ticker to quantity.
    """
    portfolio = lh.get_portfolio()
    portfolio_items = list(portfolio.items()) if portfolio else []
    return pd.DataFrame(portfolio_items, columns=['Ticker', 'Quantity'])

def placeholder_strategy():
    """
    A placeholder trading strategy that:
    1. Retrieves a list of all available tickers.
    2. Selects a random ticker.
    3. Gets the current price for that ticker.
    4. Places a buy order for one share at the current market ask.
    Returns a dictionary with trade details.
    """
    tickers = lh.get_all_tickers()
    if not tickers:
        return {"error": "No tickers found"}
    
    ticker = random.choice(tickers)
    print(f"Selected ticker: {ticker}")

    current_price = lh.get_current_price(ticker)
    price_df = pd.DataFrame(current_price['data'])
    market_ask = price_df['askMedian'].iloc[0]
    amount = 1
    
    order_response = lh.buy(ticker, amount)
    print(f"Placed buy order: {amount} share of {ticker} at {market_ask}.")
    
    return {
        "ticker": ticker,
        "amount": amount,
        "market_ask": market_ask,
        "order_response": order_response
    }
    
def sell_all_stocks():
    """
    Iterates over all positions in the portfolio and sells the entire position.
    """
    portfolio = lh.get_portfolio()
    if portfolio:
        for ticker, qty in portfolio.items():
            if qty > 0:
                lh.sell(ticker, qty)
                print(f"Sold {qty} shares of {ticker}")

@app.route('/')
def index():
    # Step 1: Get initial portfolio (should be empty)
    initial_df = get_portfolio_df()
    initial_html = initial_df.to_html(index=False)
    
    # Step 2: Execute three buy orders
    buy_messages = []
    for i in range(3):
        result = placeholder_strategy()
        if "error" not in result:
            buy_messages.append(f"Bought {result['amount']} share of {result['ticker']}")
        else:
            buy_messages.append("Trade error: " + result["error"])
        # Optional: small delay between orders (e.g., 1 second)
        time.sleep(1)
    
    # Step 3: Get portfolio after buys
    portfolio_after_buy_df = get_portfolio_df()
    portfolio_after_buy_html = portfolio_after_buy_df.to_html(index=False)
    
    # Step 4: Sell all stocks
    sell_all_stocks()
    
    # Step 5: Get portfolio after selling
    portfolio_after_sell_df = get_portfolio_df()
    portfolio_after_sell_html = portfolio_after_sell_df.to_html(index=False)
    
    # Build final HTML response
    html_response = f"""
    <html>
    <head>
        <title>Trading App - Sequential Portfolio Updates</title>
    </head>
    <body>
        <h1>Initial Portfolio</h1>
        {initial_html}
        <hr>
        <h1>Buy Orders Executed</h1>
        <ul>
            {''.join(f'<li>{msg}</li>' for msg in buy_messages)}
        </ul>
        <hr>
        <h1>Portfolio After Buys</h1>
        {portfolio_after_buy_html}
        <hr>
        <h1>Portfolio After Selling</h1>
        {portfolio_after_sell_html}
        <p>All stocks have been sold after.</p>
    </body>
    </html>
    """
    return render_template_string(html_response)

if __name__ == '__main__':
    # Run the app on host 0.0.0.0 and port 8000
    app.run(host="0.0.0.0", port=8000, debug=True)
