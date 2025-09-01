from flask import Flask, render_template, send_file
import yfinance as yf
import matplotlib.pyplot as plt
import os
import json

# Flask init
app = Flask(__name__)


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_price(self):
        try:
            ticker = yf.Ticker(self.symbol)
            current_price = ticker.info.get('currentPrice')
            return current_price
        except Exception:
            return None


def get_historical_data(symbol, period="1y"):
    try:
        data = yf.download(symbol, period=period, auto_adjust=True)
        return data
    except Exception:
        return None


def plot_stock_history_to_file(symbol, data, filename):
    if data is None or data.empty:
        return False

    plt.figure(figsize=(10, 6))
    data['Close'].plot()
    plt.title(f"Historyczne ceny akcji {symbol}")
    plt.xlabel("Data")
    plt.ylabel("Cena zamknięcia")
    plt.grid(True)

    plt.savefig(filename)
    plt.close()
    return True


CONFIG_FILE = "config.json"


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            symbols = json.load(f)
            return symbols
    except FileNotFoundError:
        return ['AAPL', 'MSFT', 'GOOGL', 'TSLA']


# --- Flask routes ---

@app.route('/')
def index():
    monitored_symbols = load_config()
    my_portfolio = []

    for symbol in monitored_symbols:
        stock = Stock(symbol)
        my_portfolio.append({
            'symbol': symbol,
            'price': stock.get_price()
        })

    return render_template('index.html', portfolio=my_portfolio)


@app.route('/wykres/<symbol>')
def show_chart(symbol):
    historical_data = get_historical_data(symbol)

    filename = f"{symbol}.png"
    filepath = os.path.join("static", filename)

    if plot_stock_history_to_file(symbol, historical_data, filepath):
        return send_file(filepath, mimetype='image/png')
    else:
        return "Nie udało się wygenerować wykresu."


if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)