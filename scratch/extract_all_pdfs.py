import os
import pypdf

pdfs = [
    "Privacy_&_Cookies_Policy.pdf",
    "Disclaimer_EFB.pdf",
    "EFB_BDP_Terms_and_Conditions.pdf",
    "BDP_Privacy_Policy.pdf"
]

for filename in pdfs:
    pdf_path = os.path.join("guides", filename)
    txt_filename = os.path.splitext(filename)[0] + ".txt"
    txt_path = os.path.join("scratch", txt_filename)
    
    print(f"Extracting {pdf_path} -> {txt_path} ...")
    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} does not exist!")
        continue
        
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- PAGE {i+1} ---\n"
        text += page.extract_text() or ""
        
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Done.")
