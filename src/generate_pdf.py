import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from utils import load_config
from llama_functions import translate_date, format_description, translate_text
from analysis import analyze_multiple_tickers, generate_stock_analysis_text

class CustomPDF(FPDF):
    def __init__(self, paths, ticker_data, language):
        super().__init__()
        self.paths = paths 
        self.language = language
        print(f"Language: {self.language}")
        self.ticker_data = ticker_data

        #self.add_font("Lato", "", os.path.abspath(os.path.join(self.paths["fonts"], "Lato-Regular.ttf")), uni=True)
        #self.add_font("Lato", "B", os.path.abspath(os.path.join(self.paths["fonts"], "Lato-Bold.ttf")), uni=True)
        #self.add_font("Lato", "BL", os.path.abspath(os.path.join(self.paths["fonts"], "Lato-Black.ttf")), uni=True)
        #self.add_font("Lato", "I", os.path.abspath(os.path.join(self.paths["fonts"], "Lato-Italic.ttf")), uni=True)

        self.set_auto_page_break(auto=True, margin=15) 

    def format_date(self):
        """Generate the date in English and translate it only if necessary."""
        date_en = datetime.now().strftime("%B %d, %Y") 

        if self.language != "english":
            return translate_date(date_en, target_language=self.language)
        
        return date_en 

    def header(self):
        """Adds a header with the current date and header image."""
        self.set_font("Arial", "B", 12)

        if os.path.exists(self.paths["header_image"]):
            self.image(self.paths["header_image"], x=0, y=0, w=210)
            self.ln(0)

        self.set_text_color(255, 255, 255)
        self.set_x(-50)
        self.cell(48, 10, f"{self.format_date()}", ln=True, align="R")

    def generate_report(self):
        """Generates a PDF report comparing tickers in a two-column format."""
        self.add_page()
        tickers = list(self.ticker_data.keys())

        for i in range(0, len(tickers), 2):
            ticker1 = tickers[i]
            ticker2 = tickers[i + 1] if i + 1 < len(tickers) else None 

            col1_x, col2_x = 5, 105
            start_y = self.get_y()

            self.add_column(ticker1, col1_x, start_y)

            if ticker2:
                self.add_column(ticker2, col2_x, start_y)

            self.ln(5)
            self.insert_financial_ratios_table(ticker1, ticker2)

            if i + 2 < len(tickers):
                self.add_page()

        # Save the PDF
        today_date = datetime.today().strftime("%Y_%m_%d")
        pdf_filename = os.path.join(self.paths["report"], f"financial_report_{today_date}.pdf")
        self.output(pdf_filename)
        print(f"PDF saved at: {pdf_filename}")


    def add_column(self, ticker, x_pos, start_y):
        """Adds a company's section (title + chart) at a fixed Y position."""
        self.set_xy(x_pos, start_y) 

        self.set_x(x_pos + 5)
        self.set_font("Arial", "B", 14)
        self.cell(90, 10, ticker, ln=True, align="C")
        self.ln(5)

        self.insert_chart(ticker, x_pos, start_y + 8) 

        self.set_font("Arial", "", 11)
        self.set_xy(x_pos + 5, self.get_y() + 5) 

        stock_prices = self.ticker_data[ticker]["Stock Prices"]
        analysis_text = generate_stock_analysis_text(ticker, stock_prices, self.language)
        if self.language == 'english':
            self.multi_cell(90, 6, analysis_text) 
        else:
            self.multi_cell(90, 6, translate_text(analysis_text, self.language)) 
        self.ln(10) 


    def insert_chart(self, ticker, x_pos, y_pos):
        """Inserts the stock price chart for a given ticker at a specific x and y position."""
        images_dir = os.path.join(self.paths["images"], "price_charts")
        matching_images = [f for f in os.listdir(images_dir) if f.startswith(ticker)]

        if not matching_images:
            self.set_xy(x_pos, y_pos)
            self.cell(90, 10, f"No plot available for {ticker}.", ln=True, align="C")
            return

        image_path = os.path.join(images_dir, matching_images[0])

        # ensure images start at the same Y level
        self.image(image_path, x=x_pos, y=y_pos, w=105, h=65)
        new_y = y_pos + 63 

        self.set_xy(x_pos + 5, new_y)  
        self.set_font("Arial", "I", 9)
        if self.language == 'english':
            self.cell(90, 5, "Source: Yahoo Finance", ln=True, align="R")
        else:
            self.cell(90, 5, translate_text("Source: Yahoo Finance", self.language), ln=True, align="R")


    def insert_financial_ratios_table(self, ticker1, ticker2):
        """Displays financial ratios in a table format with tickers as columns."""
        data1 = self.ticker_data[ticker1]["Financial Ratios"]
        data2 = self.ticker_data[ticker2]["Financial Ratios"] if ticker2 else {}

        ratio_keys = sorted(set(data1.keys()).union(set(data2.keys())))

        self.ln(5)
        self.set_font("Arial", "B", 12)
        if self.language == 'english':
            self.cell(90, 8, "Financial Ratios", border=1, align="C")
        else:    
            self.cell(90, 8, translate_text("Financial Ratios", self.language), border=1, align="C")
        self.cell(50, 8, ticker1, border=1, align="C")
        if ticker2:
            self.cell(50, 8, ticker2, border=1, align="C")
        self.ln()

        # insert each financial ratio as a row
        self.set_font("Arial", "", 10)
        for ratio in ratio_keys:
            if str(data1.get(ratio, "-")) == "N/A" or str(data2.get(ratio, "-")) == "N/A" or str(ratio) == "Market Cap (USD)" or str(ratio) == "Enterprise Value (USD)" or str(ratio) == "52-Week Low" or str(ratio) == "52-Week High":
                continue
            if self.language == "english":
                self.cell(90, 8, ratio, border=1)
            else: 
                self.cell(90, 8, translate_text(ratio, self.language), border=1)
            self.cell(50, 8, str(data1.get(ratio, "-")), border=1, align="C")
            if ticker2:
                self.cell(50, 8, str(data2.get(ratio, "-")), border=1, align="C")
            self.ln()

paths = load_config()

# example usage
if __name__ == "__main__":
    tickers = ["AAPL", "AMZN", "AMER3.SA", "LREN3.SA"]  
    ticker_data = analyze_multiple_tickers(tickers, language='pt') 

    pdf = CustomPDF(paths, ticker_data, language='pt')
    pdf.generate_report()