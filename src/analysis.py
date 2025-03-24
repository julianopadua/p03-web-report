import yfinance as yf
import pandas as pd

class StockAnalysis:
    """Fetches and analyzes stock data from Yahoo Finance."""

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        self.company_info = {}

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

    def get_stock_price_series(self, period="1y", interval="1d"):
        """Fetches historical stock prices."""
        try:
            df = self.stock.history(period=period, interval=interval)[["Close"]]
            df.index = pd.to_datetime(df.index)
        except Exception as e:
            print(f"⚠️ Error fetching stock data for {self.ticker}: {e}")
            df = pd.DataFrame()

        return df

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


def analyze_multiple_tickers(tickers):
    """Fetches data for multiple tickers."""
    results = {}

    for ticker in tickers:
        stock = StockAnalysis(ticker)
        results[ticker] = {
            "Description": stock.get_company_description(),
            "Stock Prices": stock.get_stock_price_series(),
            "Financial Ratios": stock.get_financial_ratios(),
        }

    return results


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

        print("\n" + "=" * 50)
