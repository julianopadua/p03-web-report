import os
from fpdf import FPDF
from datetime import datetime
from utils import load_config
from llama_functions import translate_date

class CustomPDF(FPDF):
    def __init__(self, paths, language="en"):
        super().__init__()
        self.paths = paths  # Load all necessary paths
        self.language = language

        self.add_font("Lato", "", os.path.join(self.paths["fonts"], "Lato-Regular.ttf"), uni=True)
        self.add_font("Lato", "B", os.path.join(self.paths["fonts"], "Lato-Bold.ttf"), uni=True)
        self.add_font("Lato", "BL", os.path.join(self.paths["fonts"], "Lato-Black.ttf"), uni=True)

        self.set_auto_page_break(auto=True, margin=15)  # Ensure content doesn't overlap footer

    def format_date(self):
        """Generate the date in English and translate it only if necessary."""
        date_en = datetime.now().strftime("%B %d, %Y")  # ✅ Always generate in English

        # ✅ Only translate if the language is NOT English
        if self.language != "en":
            return translate_date(date_en, target_language=self.language)
        
        return date_en 

    def header(self):
        """Adds a header with the current date and header image."""
        self.set_font("Lato", "B", 12)

        # Add header image
        if os.path.exists(self.paths["header_image"]):
            self.image(self.paths["header_image"], x=0, y=0, w=210)
            self.ln(0)

        # Add formatted date below image
        self.set_text_color(255, 255, 255)
        self.set_x(-50)
        self.cell(48, 10, f"{self.format_date()}", ln=True, align="R")

    def generate_report(self, title, content):
        """Generates a PDF report with headers on each page."""
        self.add_page()  # Each new page automatically calls `header()`

        # Title
        self.set_font("Lato", "B", 16)
        self.cell(0, 10, title, ln=True, align="C")

        self.ln(10)  # Space after title
        self.set_font("Lato", "", 12)

        # Add Content
        for line in content:
            self.multi_cell(0, 10, line)
            self.ln(2)

        # Save PDF in the report folder
        pdf_filename = os.path.join(self.paths["report"], "financial_report.pdf")
        self.output(pdf_filename)
        print(f"✅ PDF saved at: {pdf_filename}")

# 1️⃣ Load centralized paths from utils.py
paths = load_config()

# 2️⃣ Generate PDF Example
if __name__ == "__main__":
    pdf = CustomPDF(paths)

    content = [
        "This is a financial report generated using FPDF and Python.",
        "It includes a dynamic header with an image and the current date on every page.",
        "This example demonstrates multi-page content handling.",
        "\n".join(["More sample text to force a page break."] * 50)  # Forces multiple pages
    ]

    pdf.generate_report("Financial Report", content)
