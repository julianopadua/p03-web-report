# Made by Juliano E. S. Padua
import streamlit as st
import pandas as pd
import datetime
import os
from utils import load_config
from generate_pdf import analyze_multiple_tickers, CustomPDF  # Importing PDF generation functions

paths = load_config()

STOCKS_CSV = os.path.join(paths["data_processed"], "stocks.csv")

def load_tickers():
    """Load tickers from stocks.csv and return a sorted list."""
    if os.path.exists(STOCKS_CSV):
        df = pd.read_csv(STOCKS_CSV)
        if "Name" in df.columns:
            return sorted(df["Name"].dropna().unique().tolist())  # Ensure no duplicates and sorted
    return []  # Return an empty list if file not found

TICKER_LIST = load_tickers()

LANGUAGE_OPTIONS = {
    "English": "english",
    "Português (Brasil)": "pt",
    "Español": "spanish",
    "Français": "french",
    "Deutsch": "de",
    "Italiano": "italian"
}

# initial setup
st.set_page_config(page_title="Company Comparison Report", layout="wide")
st.title("📊 Company Comparison Report")
st.write("Select companies and a language for generating a financial report.")

#dropdown for tickers
selected_tickers = st.multiselect(
    "Search and Select Company Tickers", 
    options=TICKER_LIST, 
    default=[], 
    placeholder="Type to search (e.g., AAPL, GOOGL) or enter manually"
)

# manually add a ticker
manual_ticker = st.text_input("Or enter one or more tickers manually (comma-separated, e.g., GOOG, AAPL, AMZN)")

if manual_ticker:
    tickers = [t.strip().upper() for t in manual_ticker.split(",") if t.strip()]
    print(f"TICKERS: {tickers}")
    # append would add the list itself as the next element of selected tickers;
    # extend iterate through tickers and add one-by-one
    selected_tickers.extend(tickers)  
 

# Remove duplicates if a ticker is both in dropdown and manually added
selected_tickers = list(set(selected_tickers))

### 2. Searchable Dropdown for Language Selection
selected_language = st.selectbox(
    "🌍 Choose Report Language",
    options=list(LANGUAGE_OPTIONS.keys()),
    index=0  # Default to English
)

### 3. Display Selections
st.write("### Selected Parameters:")
st.write(f"**📌 Companies:** {', '.join(selected_tickers) if selected_tickers else 'None selected'}")
st.write(f"**📌 Language:** {selected_language} ({LANGUAGE_OPTIONS[selected_language]})")

### 4. Generate Report Button (Enabled only if selections are valid)
if selected_tickers and selected_language:
    if st.button("📝 Generate Report"):
        st.success("✅ Report is being generated... Please wait.")

        # Call PDF generation
        ticker_data = analyze_multiple_tickers(selected_tickers, language=LANGUAGE_OPTIONS[selected_language])
        pdf = CustomPDF(paths, ticker_data, language=LANGUAGE_OPTIONS[selected_language])
        pdf.generate_report()

        today_date = datetime.datetime.now().strftime("%Y_%m_%d")  # Format: YYYY_MM_DD
        pdf_filename = f"financial_report_{today_date}.pdf"  # Define a name for the report
        pdf_path = os.path.join(paths["report"], pdf_filename)

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Report",
                    data=pdf_file,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
        else:
            st.error("⚠️ Report generation failed. Please try again.")

# Footer
st.markdown("---")
st.write(f"Project **p03-web-report** initialized on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
