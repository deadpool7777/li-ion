import fitz  # PyMuPDF
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Step 1: Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

pdf_path = r"C:\Users\Alwin Soly\Desktop\li-ion\s42452-020-2675-6.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

# Step 2: Loading the pre-trained model and tokenizer
model_name = "batterydata/batterybert-cased-squad-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Step 3: Create a text classification pipeline
battery_data_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)

# Step 4: Analyze the extracted text
def analyze_text(pipeline, text, chunk_size=512):
    results = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        result = pipeline(chunk)
        results.extend(result)
    return results

# Analyze the extracted text
results = analyze_text(battery_data_pipeline, extracted_text)

# Save the results to a text file
# output_file_path = r"C:\Users\Alwin Soly\Desktop\battery_data_analysis_results.txt"
# with open(output_file_path, "w") as file:
#     for res in results:
#         file.write(f"Label: {res['label']}, Score: {res['score']}\n")
