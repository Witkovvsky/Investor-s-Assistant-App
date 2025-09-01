import requests
import json
import matplotlib.pyplot as plt
import datetime
import yfinance as yf


# Klasa do reprezentowania pojedynczej akcji (uproszczona dla yfinance)
CONFIG_FILE = "config.json"


# --- Funkcje do obsługi plików konfiguracyjnych ---
class Stock:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_price(self):
        """Pobiera aktualną cenę z Yahoo Finance."""
        try:
            # Użycie yfinance do pobrania bieżących danych
            ticker = yf.Ticker(self.symbol)
            current_price = ticker.info.get('currentPrice')

            if current_price:
                print(f"Aktualna cena akcji {self.symbol} to: {current_price}")
                return current_price
            else:
                print(f"Nie udało się pobrać ceny dla symbolu {self.symbol}.")
                return None
        except Exception as e:
            print(f"Błąd podczas pobierania danych dla {self.symbol}: {e}")
            return None


def save_config(symbols):
    """Zapisuje listę symboli do pliku JSON."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(symbols, f, indent=4)
    print("Konfiguracja została zapisana.")


def load_config():
    """Wczytuje listę symboli z pliku JSON. Zwraca pustą listę, jeśli plik nie istnieje."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            symbols = json.load(f)
            return symbols
    except FileNotFoundError:
        print("Brak pliku konfiguracyjnego. Tworzę nową listę.")
        return []


# --- Funkcja do wizualizacji danych ---
def plot_stock_history_to_file(symbol, data, filename="static/wykres.png"):
    if data is None or data.epmty:
        print("Brak danych do wygenerowania wykresu.")
        return

    prices = data['Close']

    plt.figure(figsize=(10, 6))
    prices.plot()
    plt.title(f"Historyczne ceny akcji {symbol}")
    plt.xlabel("Data")
    plt.ylabel("Cena zamknięcia")
    plt.grid(True)

    plt.savefig(filename)
    plt.close()
    return True


# --- Główny blok uruchomieniowy ---
if __name__ == "__main__":
    print("Sprawdzanie i ładowanie konfiguracji...")
    monitored_symbols = load_config()

    if not monitored_symbols:
        print("Lista monitorowanych symboli jest pusta. Dodaję domyślne symbole.")
        monitored_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
        save_config(monitored_symbols)

    my_portfolio = []
    print("\nPobieram aktualne ceny dla monitorowanych akcji...")
    for symbol in monitored_symbols:
        stock = Stock(symbol)
        stock.get_price()
        my_portfolio.append(stock)

    print("\n--- Podsumowanie portfela ---")
    for stock in my_portfolio:
        print(f"Symbol: {stock.symbol}, Cena: {stock.get_price()}")

    # Wizualizacja danych historycznych dla pierwszej akcji
    if monitored_symbols:
        symbol_to_plot = monitored_symbols[0]
        print(f"\nPobieram dane historyczne dla {symbol_to_plot} i generuję wykres...")

        # Pobieranie danych historycznych za ostatni rok
        historical_data = yf.download(symbol_to_plot, period="1y", auto_adjust=True)
        plot_stock_history(symbol_to_plot, historical_data)