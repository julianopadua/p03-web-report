import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils import load_config
from llama_functions import translate_chart_labels, format_stock_analysis

# Load paths from config.yaml
paths = load_config()

class StockAnalysis:
    """Fetches and analyzes stock data from Yahoo Finance."""

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        self.company_info = {}
        self.stock_prices = pd.DataFrame()

        # Define output folder for plots
        self.plot_path = os.path.join(paths["price_charts"], f"{self.ticker}_price_chart.png")

    def get_company_description(self):
        """Fetches company information (Stored in English)."""
        try:
            info = self.stock.info
            self.company_info = {
                "Name": info.get("longName", "N/A"),
                "Summary": info.get("longBusinessSummary", "N/A"),
                "Industry": info.get("industry", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Employees": info.get("fullTimeEmployees", "N/A"),
                "Country": info.get("country", "N/A"),
                "Website": info.get("website", "N/A"),
            }
        except Exception as e:
            print(f"⚠️ Error fetching description for {self.ticker}: {e}")
            self.company_info = {}

        return self.company_info

    def get_stock_price_series(self, language, period="1y", interval="1d"):
        """Fetches historical stock prices, saves it as a CSV, and generates a plot."""
        try:
            self.stock_prices = self.stock.history(period=period, interval=interval)[["Close"]]
            self.stock_prices.index = pd.to_datetime(self.stock_prices.index)

            # ✅ Generate and save plot
            self.save_stock_price_plot(language)

        except Exception as e:
            print(f"⚠️ Error fetching stock data for {self.ticker}: {e}")
            self.stock_prices = pd.DataFrame()

        return self.stock_prices

    def save_stock_price_plot(self, language="en"):
        """Generates and saves a stock price plot with translated labels."""
        if not self.stock_prices.empty:
            # ✅ Define default labels (without ticker in title)
            labels = {
                "title": "Stock Price Over Time",  # Remove ticker for translation
                "y_axis": "Closing Price (USD)"
            }

            # ✅ Translate labels if language is not English
            if language != "en":
                translated_labels = translate_chart_labels(labels, target_language=language)
            else:
                translated_labels = labels  # No translation needed

            # ✅ Re-add the ticker to the translated title
            translated_title = f"{self.ticker} - {translated_labels['title']}"

            # ✅ Generate plot with new styles
            plt.figure(figsize=(10, 5))
            plt.plot(self.stock_prices.index, self.stock_prices["Close"], label=self.ticker, color="red", linewidth=2.5)  # ✅ Thicker red line
            plt.title(translated_title, fontsize=18)
            plt.ylabel(translated_labels["y_axis"], fontsize=16) 
            plt.legend(fontsize=12)
            plt.grid(False)

            # ✅ Save the translated plot
            plt.savefig(self.plot_path)
            plt.close()  # Free memory
            print(f"✅ Saved stock price plot for {self.ticker} in {language}: {self.plot_path}")
        else:
            print(f"⚠️ No data to plot for {self.ticker}.")

    def get_financial_ratios(self):
        """Fetches financial ratios (P/E, ROE, etc.)."""
        try:
            info = self.stock.info
            financials = {
                "Market Cap (USD)": info.get("marketCap", "N/A"),
                "Enterprise Value (USD)": info.get("enterpriseValue", "N/A"),
                "Price-to-Book (P/B)": info.get("priceToBook", "N/A"),
                "Price-to-Earnings (P/E)": info.get("trailingPE", "N/A"),
                "Forward P/E": info.get("forwardPE", "N/A"),
                "PEG Ratio": info.get("pegRatio", "N/A"),
                "Return on Equity (ROE)": info.get("returnOnEquity", "N/A"),
                "Debt-to-Equity Ratio": info.get("debtToEquity", "N/A"),
                "Profit Margin": info.get("profitMargins", "N/A"),
                "Dividend Yield": info.get("dividendYield", "N/A"),
                "52-Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "52-Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                "Beta (Volatility)": info.get("beta", "N/A"),
            }
        except Exception as e:
            print(f"⚠️ Error fetching financial ratios for {self.ticker}: {e}")
            financials = {}

        return financials


def analyze_multiple_tickers(tickers, language):
    """Fetches data for multiple tickers and saves organized CSV files."""
    results = {}

    output_dir = os.path.join(paths["data_processed"])
    os.makedirs(output_dir, exist_ok=True)

    for ticker in tickers:
        stock = StockAnalysis(ticker)
        
        # Gather data
        description = stock.get_company_description()
        financial_ratios = stock.get_financial_ratios()
        plot_path = stock.plot_path  # ✅ Store plot path for reference

        results[ticker] = {
            "Description": description,
            "Stock Prices": stock.get_stock_price_series(language),
            "Financial Ratios": financial_ratios,
            "Plot Path": plot_path,
        }
    
    return results

def generate_stock_analysis_text(ticker, stock_prices):
    """
    Generates a conditional text analysis based on stock price movements.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL").
        stock_prices (pd.DataFrame): DataFrame containing historical stock prices 
                                     with a "Close" column.

    Returns:
        str: Analysis text summarizing key stock price movements.
    """
    if stock_prices is None or stock_prices.empty:
        return f"No stock price data available for {ticker}."

    # ✅ Extract relevant price points
    latest_close = stock_prices["Close"].iloc[-1]
    one_week_ago = stock_prices["Close"].iloc[-6] if len(stock_prices) > 6 else None
    one_month_ago = stock_prices["Close"].iloc[-22] if len(stock_prices) > 22 else None
    one_year_ago = stock_prices["Close"].iloc[-252] if len(stock_prices) > 252 else None

    # ✅ 52-week high & low
    high_52w = stock_prices["Close"].rolling(window=252, min_periods=1).max().iloc[-1]
    low_52w = stock_prices["Close"].rolling(window=252, min_periods=1).min().iloc[-1]

    # ✅ Moving Averages
    ma_5 = stock_prices["Close"].rolling(window=5).mean().iloc[-1]
    ma_10 = stock_prices["Close"].rolling(window=10).mean().iloc[-1]
    ma_30 = stock_prices["Close"].rolling(window=30).mean().iloc[-1]

    # 🔹 Start generating text
    text = f"{ticker} closed at {latest_close:.2f} USD.\n"

    # ✅ 52-week high/low comparison
    if latest_close == high_52w:
        text += "This is the highest closing price in the past 52 weeks!\n"
    else:
        diff_high = high_52w - latest_close
        text += f"This price is {diff_high:.2f} USD below the 52-week high of {high_52w:.2f}.\n"

    if latest_close == low_52w:
        text += "This is the lowest closing price in the past 52 weeks!\n"
    else:
        diff_low = latest_close - low_52w
        text += f"This price is {diff_low:.2f} USD above the 52-week low of {low_52w:.2f}.\n"

    # ✅ Week-over-week comparison
    if one_week_ago:
        week_diff = latest_close - one_week_ago
        direction = "above" if week_diff > 0 else "below"
        text += f"Today's close was {abs(week_diff):.2f} USD {direction} last week's close of {one_week_ago:.2f}.\n"

    # ✅ Month-over-month comparison
    if one_month_ago:
        month_diff = latest_close - one_month_ago
        direction = "above" if month_diff > 0 else "below"
        text += f"Today's close was {abs(month_diff):.2f} USD {direction} the close one month ago ({one_month_ago:.2f}).\n"

    # ✅ Year-over-year comparison
    if one_year_ago:
        year_diff = latest_close - one_year_ago
        direction = "above" if year_diff > 0 else "below"
        text += f"Today's close was {abs(year_diff):.2f} USD {direction} the close one year ago ({one_year_ago:.2f}).\n"

    # ✅ Moving Average Analysis
    if latest_close > ma_5:
        text += f"The stock is currently trading above its 5-day moving average ({ma_5:.2f}).\n"
    else:
        text += f"The stock is below its 5-day moving average ({ma_5:.2f}).\n"

    if latest_close > ma_10:
        text += f"It is also above the 10-day moving average ({ma_10:.2f}).\n"
    else:
        text += f"It is below the 10-day moving average ({ma_10:.2f}).\n"

    if latest_close > ma_30:
        text += f"The stock remains above the 30-day moving average ({ma_30:.2f}).\n"
    else:
        text += f"The stock is trading below the 30-day moving average ({ma_30:.2f}).\n"

    return format_stock_analysis(text)


if __name__ == "__main__":
    # Example Usage (Testing)
    tickers = ["AAPL", "GOOGL"]
    results = analyze_multiple_tickers(tickers)

    for ticker, data in results.items():
        print("\n" + "=" * 50)
        print(f"📌 {ticker} - {data['Description'].get('Name', 'N/A')}")
        print("=" * 50)

        # 📖 Company Description
        print(f"\n📝 **Company Description:**\n{data['Description'].get('Summary', 'N/A')}")
        print(f"🔹 Sector: {data['Description'].get('Sector', 'N/A')}")
        print(f"🔹 Industry: {data['Description'].get('Industry', 'N/A')}")
        print(f"🔹 Employees: {data['Description'].get('Employees', 'N/A')}")
        print(f"🔹 Country: {data['Description'].get('Country', 'N/A')}")
        print(f"🔹 Website: {data['Description'].get('Website', 'N/A')}")

        # 💰 Financial Ratios
        print("\n📊 **Financial Ratios:**")
        for key, value in data["Financial Ratios"].items():
            print(f"🔹 {key}: {value}")

        # 📈 Stock Price Series (Last 5 Data Points)
        stock_prices = data["Stock Prices"]
        if not stock_prices.empty:
            print("\n📈 **Stock Price Series (Last 5 Days):**")
            print(stock_prices.tail(5))
        else:
            print("\n⚠️ No stock price data available.")

        # 📊 Saved Plot Path
        print(f"\n🖼️ Stock price plot saved at: {data['Plot Path']}")

        print("\n" + "=" * 50)
