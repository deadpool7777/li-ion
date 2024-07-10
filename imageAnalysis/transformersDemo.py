from transformers import pipeline, BartTokenizer
import fitz  # PyMuPDF

# Step 1: Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Step 2: Load the summarization pipeline and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
summarization_pipeline = pipeline("summarization", model=model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

# Function to chunk text based on tokens
def chunk_text(text, tokenizer, max_tokens=1024):
    words = text.split()
    current_chunk = []
    current_length = 0
    chunks = []

    for word in words:
        word_length = len(tokenizer.encode(word, add_special_tokens=False))
        if current_length + word_length <= max_tokens:
            current_chunk.append(word)
            current_length += word_length
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

pdf_path = r"C:\Users\Alwin Soly\Desktop\li-ion\s42452-020-2675-6.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

# Step 3: Chunk the text based on tokens
text_chunks = chunk_text(extracted_text, tokenizer)

# Step 4: Summarize each chunk
summaries = []
for chunk_text in text_chunks:
    summary = summarization_pipeline(chunk_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    summaries.append(summary)

# Step 5: Save the summaries to a text file
output_file_path = r"C:\Users\Alwin Soly\Desktop\battery_data_summary.txt"
with open(output_file_path, "w",encoding="utf-8") as file:
    for summary in summaries:
        file.write(summary + "\n\n")

print(f"Summaries saved to {output_file_path}")
