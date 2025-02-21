# Trading App

A simple Flask-based trading application that demonstrates a placeholder strategy:
- It initially shows an empty portfolio.
- It executes three buy orders.
- It displays the portfolio after buying.
- It sells all stocks.
- It then shows the final (empty) portfolio.

## Setup

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Brunstorp/example-hackathon-app.git
   cd example-hackathon-app

2. **Install Dependenvies with Pipenv**
   ```bash
   pip install pipenv
   pipenv install requirements.txt

3. **Configure Environment Variables**
   Create a .env file in the project root with your API key:
   ```bash
   API_KEY=your_api_key_here

4. **Run the Application**
   ```bash
   pipenv run python app.py

## How It Works

### Initial Portfolio
The application begins by displaying your portfolio, which should be empty if no positions exist.

### Buy Orders
The app then executes three buy orders using a placeholder strategy and logs messages like "Bought 1 share of TICKER" for each trade.

### Portfolio Updates
The portfolio is displayed after the buy orders. After a 20-second delay, the app sells all stocks and shows the final portfolio, which should now be empty.


