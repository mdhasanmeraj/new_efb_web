import os
import sys

pdf_path = os.path.join("guides", "Terms_and_Conditions_EFB.pdf")
print("PDF Path:", pdf_path)
print("Exists:", os.path.exists(pdf_path))

# Try pypdf first
try:
    import pypdf
    print("pypdf available")
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- PAGE {i+1} ---\n"
        text += page.extract_text() or ""
    with open("scratch/extracted_terms.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Extracted successfully using pypdf")
    sys.exit(0)
except ImportError:
    print("pypdf not available")

# Try PyPDF2
try:
    import PyPDF2
    print("PyPDF2 available")
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- PAGE {i+1} ---\n"
        text += page.extract_text() or ""
    with open("scratch/extracted_terms.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Extracted successfully using PyPDF2")
    sys.exit(0)
except ImportError:
    print("PyPDF2 not available")

# Try pdfplumber
try:
    import pdfplumber
    print("pdfplumber available")
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for i, page in enumerate(pdf.pages):
            text += f"--- PAGE {i+1} ---\n"
            text += page.extract_text() or ""
        with open("scratch/extracted_terms.txt", "w", encoding="utf-8") as f:
            f.write(text)
    print("Extracted successfully using pdfplumber")
    sys.exit(0)
except ImportError:
    print("pdfplumber not available")

# Try fitz (PyMuPDF)
try:
    import fitz
    print("fitz available")
    doc = fitz.open(pdf_path)
    text = ""
    for i, page in enumerate(doc):
        text += f"--- PAGE {i+1} ---\n"
        text += page.get_text() or ""
    with open("scratch/extracted_terms.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Extracted successfully using fitz")
    sys.exit(0)
except ImportError:
    print("fitz not available")

print("No known PDF extraction library available. Let's try installing pypdf...")
