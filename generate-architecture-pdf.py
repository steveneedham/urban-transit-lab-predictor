#!/usr/bin/env python3
"""
Generate PDF from system-architecture.html using available tools.
Run: python3 generate-architecture-pdf.py
"""

import subprocess
import sys
from pathlib import Path

def generate_pdf():
    html_file = Path("system-architecture.html").absolute()
    pdf_file = Path("system-architecture.pdf").absolute()

    if not html_file.exists():
        print(f"Error: {html_file} not found")
        sys.exit(1)

    # Try different tools in order of preference
    tools = [
        # wkhtmltopdf
        {
            "name": "wkhtmltopdf",
            "check": ["wkhtmltopdf", "--version"],
            "cmd": ["wkhtmltopdf", str(html_file), str(pdf_file)]
        },
        # Google Chrome/Chromium headless
        {
            "name": "chromium",
            "check": ["chromium", "--version"],
            "cmd": ["chromium", "--headless", "--disable-gpu", f"--print-to-pdf={pdf_file}", str(html_file)]
        },
        # Chrome (macOS)
        {
            "name": "Google Chrome",
            "check": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
            "cmd": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu", f"--print-to-pdf={pdf_file}", str(html_file)]
        }
    ]

    for tool in tools:
        try:
            # Check if tool is available
            subprocess.run(tool["check"], capture_output=True, timeout=5)
            print(f"✓ Found {tool['name']}, generating PDF...")
            result = subprocess.run(tool["cmd"], capture_output=True, timeout=30)

            if result.returncode == 0 and pdf_file.exists():
                print(f"✓ PDF generated: {pdf_file}")
                print(f"  File size: {pdf_file.stat().st_size / 1024:.1f} KB")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

    print("No PDF generation tools found. Available options:")
    print("1. Install wkhtmltopdf: https://wkhtmltopdf.org/")
    print("2. Install Chromium: apt-get install chromium-browser")
    print("3. Open system-architecture.html in your browser and use Print > Save as PDF")
    sys.exit(1)

if __name__ == "__main__":
    generate_pdf()
