# Made by Juliano E. S. Padua
import streamlit as st
import pandas as pd
import datetime
import os
from utils import load_config

# Load configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(script_dir, "config.yaml")
config = load_config(config_dir)

# Initialize paths from config
data_raw_path = os.path.join(script_dir, config['paths']['data_raw'])
data_processed_path = os.path.join(script_dir, config['paths']['data_processed'])
images_path = os.path.join(script_dir, config['paths']['images'])
report_path = os.path.join(script_dir, config['paths']['report'])
addons_path = os.path.join(script_dir, config['paths']['addons'])

# Set up the Streamlit page
st.set_page_config(page_title="Company Comparison App", layout="wide")

st.title("📊 Company Comparison Web App")
st.write("Select companies and languages for generating a financial report.")

### ✅ 1. Searchable Dropdown for Ticker Selection
# Load ticker list (can be from API, database, or a static list)
TICKER_LIST = [
    "AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NVDA", "BRK.A", "JPM", "V",
    "UNH", "PG", "XOM", "JNJ", "WMT", "BAC", "HD", "PFE", "KO", "PEP"
]  # Example list, you can expand

selected_tickers = st.multiselect(
    "🔍 Search and Select Company Tickers", 
    options=TICKER_LIST, 
    default=[], 
    placeholder="Type to search (e.g., AAPL, GOOGL)"
)

### ✅ 2. Searchable Dropdown for Language Selection
LANGUAGE_OPTIONS = {
    "English": "en",
    "Português (Brasil)": "pt",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "中文 (Chinese)": "zh",
    "日本語 (Japanese)": "ja",
    "Русский (Russian)": "ru",
    "हिन्दी (Hindi)": "hi",
    "العربية (Arabic)": "ar"
}

selected_language = st.selectbox(
    "🌍 Choose Report Language",
    options=list(LANGUAGE_OPTIONS.keys()),
    index=0,  # Default to English
    placeholder="Start typing (e.g., 'Port...')"
)

### ✅ 3. Display Selections and Generate Report Button
st.write("### Selected Parameters:")
st.write(f"**📌 Companies:** {', '.join(selected_tickers) if selected_tickers else 'None selected'}")
st.write(f"**📌 Language:** {selected_language} ({LANGUAGE_OPTIONS[selected_language]})")

# Generate Report Button
if st.button("📝 Generate Report"):
    if not selected_tickers:
        st.error("⚠️ Please select at least one company ticker!")
    else:
        st.success("✅ Report is being generated... (Placeholder for PDF generation)")
        # Here, call your report generation function
        # generate_pdf_report(selected_tickers, LANGUAGE_OPTIONS[selected_language])

# Footer
st.markdown("---")
st.write(f"Project **p03-web-report** initialized on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
