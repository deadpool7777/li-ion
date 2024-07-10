import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

pdf_path = r"C:\Users\Alwin Soly\Desktop\li-ion\s42452-020-2675-6.pdf"
text = extract_text_from_pdf(pdf_path)
print(text)
