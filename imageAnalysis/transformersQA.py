import fitz  # PyMuPDF
import re
from transformers import pipeline

# Step 1: Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

pdf_path = r"C:\Users\Alwin Soly\Desktop\li-ion\s42452-020-2675-6.pdf"
text = extract_text_from_pdf(pdf_path)

# Step 2: Preprocess Text
def preprocess_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

cleaned_text = preprocess_text(text)

# Step 3: Use NLP Models to Extract Information
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

questions = [
    "What is the nominal capacity of the NCR18650B battery?",
    "What is the nominal voltage of the NCR18650B battery?",
    "What are the applications of the NCR18650B battery?",
    "What is the cycle life of the NCR18650B battery?",
    "Who produces the NCR18650B battery?"
]

for question in questions:
    result = qa_pipeline(question=question, context=cleaned_text)
    print(f"Q: {question}")
    print(f"A: {result['answer']}\n")

# Step 4: Summarize Extracted Information
# summarization_pipeline = pipeline("summarization")

# summary = summarization_pipeline(cleaned_text, max_length=150, min_length=50, do_sample=False)
# print("Summary:")
# print(summary[0]['summary_text'])

# Save the final summary to a text file
# output_file = r"C:\Users\Alwin Soly\Desktop\li-ion\summary.txt"
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write(summary)

# print(f"Summary saved to {output_file}")