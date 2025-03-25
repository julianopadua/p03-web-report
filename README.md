# p03-web-report

A **Streamlit** application that compares multiple companies' financial data, generates plots and analysis, and produces a **multi-language PDF report**.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Directory Structure](#directory-structure)  
4. [Installation & Setup (Virtual Environment)](#installation--setup-virtual-environment)  
5. [Usage](#usage)  
   - [Run the Streamlit App](#run-the-streamlit-app)  
   - [Generate PDF Reports](#generate-pdf-reports)  
6. [File Explanations](#file-explanations)  
   - [6.1 `utils.py`](#61-utilspy)  
   - [6.2 `analysis.py`](#62-analysispy)  
   - [6.3 `llama_functions.py`](#63-llama_functionspy)  
   - [6.4 `generate_pdf.py`](#64-generate_pdfpy)  
   - [6.5 `streamlit_app.py`](#65-streamlit_apppy)  
7. [Future Improvements](#future-improvements)  

---

## Overview

**p03-web-report** is a **full-stack financial data analysis project** for:

1. **Managing** a CSV file of stock symbols (located in `data/processed/stocks.csv`).  
2. **Fetching** financial and descriptive data from Yahoo Finance.  
3. **Generating** line charts and summary analytics.  
4. **Translating** descriptions and analysis into multiple languages (e.g., English, Portuguese, Spanish, French, German, Italian) via a **LLaMA** API.  
5. **Combining** data into a **PDF report** with side-by-side comparisons of selected tickers.  
6. **Providing** a user-friendly **Streamlit web app** to select tickers, choose a language, and download a final PDF.

---

## Features

- **Dynamic Ticker Input**  
  Pick from the **stocks.csv** or manually type your own.
- **Multi-Language Support**  
  Translate chart labels, company descriptions, and analysis text into your chosen language.
- **PDF Reporting**  
  Generate a polished, corporate-style PDF with charts, ratios, and curated analysis.
- **Streamlit Front-End**  
  Simple, interactive interface for selecting tickers and finalizing your custom report.

---

## Directory Structure

Below is an example layout of the project:

```
p03-web-report/
│
├─ src/
│   ├─ streamlit_app.py          # Main Streamlit application
│   ├─ generate_pdf.py           # PDF generation logic
│   ├─ analysis.py               # Fetching & analyzing data
│   ├─ llama_functions.py        # LLaMA-based translation & formatting
│   ├─ utils.py                  # Config loading & path handling
│   ├─ config.yaml               # Config settings (paths, API keys, etc.)
│   └─ requirements.txt          # Dependencies (optional)
│
├─ data/
│   ├─ processed/                # Contains stocks.csv
│   └─ (any other subfolders)
├─ report/                       # PDF reports saved here
├─ images/
│   ├─ header.png                # Header image for PDF
│   └─ price_charts/            # Folder for generated line charts
├─ fonts/                        # Custom fonts (e.g., Lato)
└─ README.md
```

---

## Installation & Setup (Virtual Environment)

1. **Clone or Download** this repository to your local machine.

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   ```
   
3. **Activate the Virtual Environment**:
   - **Windows (CMD):**
     ```bash
     venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     venv\Scripts\Activate.ps1
     ```
     *If you get a permission error, run:*
     ```powershell
     Set-ExecutionPolicy Unrestricted -Scope Process
     ```
   - **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies** (if you have a `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
   Otherwise, install packages manually:
   ```bash
   pip install streamlit pandas requests beautifulsoup4 yfinance matplotlib fpdf pyyaml
   ```
5. **Add Your API Key(s)** in `config.yaml` (under `api_keys`) to enable LLaMA translations.

---

## Usage

### Run the Streamlit App

1. **Ensure** your virtual environment is **active**.
2. **Navigate** to the `src` directory:
   ```bash
   cd src
   ```
3. **Launch** the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
4. **Open** the URL shown in your terminal (e.g., `http://localhost:8501`).

**In the Streamlit UI**:
1. **Select/Type** the ticker symbols you want to compare.  
2. **Pick** the desired language.  
3. Click **"Generate Report"** → A new PDF is created.  
4. **Download** your PDF via the download button.

### Generate PDF Reports

If you’d like to generate PDFs **directly** from the command line (bypassing the Streamlit UI), you can run:
```bash
python generate_pdf.py
```
This script uses functions from `analysis.py` and `llama_functions.py` to build the final PDF report.

---

## File Explanations

### 6.1 `utils.py`

**Purpose**:  
- Reads `config.yaml` to load **paths** for storing PDF files, images, fonts, etc.  
- Ensures directories exist (e.g., `report` folder).  

```python
def load_config():
    # 1. Construct path to config.yaml
    # 2. Read the YAML file
    # 3. Return a 'paths' dictionary with absolute directories
```

### 6.2 `analysis.py`

**Purpose**:  
- Connects to **Yahoo Finance** to fetch company info, historical prices, and key financial ratios.  
- Generates **line charts** saved in `images/price_charts/`.

**Key Classes/Functions**:  
- `StockAnalysis(ticker)`:  
  - **get_company_description()**: Basic company info.  
  - **get_stock_price_series(language, period, interval)**: Fetch daily/weekly data.  
  - **save_stock_price_plot(language)**: Creates & saves a price chart.  
  - **get_financial_ratios()**: Retrieves ratios like P/E, PEG, etc.

- `analyze_multiple_tickers(tickers, language)`:  
  - Loops through each ticker.  
  - Returns a dictionary of results for further processing.

- `generate_stock_analysis_text(ticker, stock_prices)`:  
  - Summarizes price movements (52-week highs/lows, moving averages, etc.).

### 6.3 `llama_functions.py`

**Purpose**:  
- Integrates with a **LLaMA** (Groq) model to translate and/or refine text.  
- **translate_text()** and **translate_chart_labels()** for charting or user interface.  
- **format_description()** and **format_stock_analysis()** to produce more professional, concise text.

### 6.4 `generate_pdf.py`

**Purpose**:  
- Uses the `FPDF` library to build a **multi-page, multi-column PDF** with textual and graphical data.  
- Pulls data from `analysis.py` for each ticker, organizes it side-by-side.

**Key Class**: `CustomPDF`:
- **header()**: Adds a date (in the chosen language) and optional header image.  
- **generate_report()**: Creates the entire multi-ticker PDF.  
- **add_column()**, **insert_chart()**, **insert_financial_ratios_table()**: Helpers for layout and styling.

### 6.5 `streamlit_app.py`

**Purpose**:  
- Provides a **user interface** for ticker selection, language choice, and PDF downloading.

**Core Steps**:
1. **Load** `stocks.csv` from `data/processed` to populate the ticker list.  
2. **Multiselect** widget to pick multiple tickers.  
3. **Language** dropdown for translation.  
4. **Generate Report** button → calls the PDF creation, then offers a download link.

---

## Future Improvements

- **Add More Technical Indicators** in charts (RSI, MACD, volume bars, etc.).  
- **Advanced PDF Layout** (e.g., custom sections, clickable table of contents).  
- **Database Integration** to track and store user preferences or watchlists.  
- **Auto-Deployment** to Streamlit Cloud or other platforms for public usage.

---