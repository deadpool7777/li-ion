import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

# Function to clean text
def clean_text(text):
    # Remove HTML tags if any (though BeautifulSoup is better for this purpose)
    text = re.sub(r'<.*?>', '', text)
    # Remove non-alphanumeric characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text.lower())
    return text

# Function to tokenize text
def tokenize_text(text):
    tokens = word_tokenize(text)
    # Remove stopwords and punctuation
    tokens = [token for token in tokens if token not in stopwords.words('english') + list(string.punctuation)]
    return tokens

# Function to process paragraphs
def process_paragraphs(paragraphs):
    # Join paragraphs into a single text
    text = ' '.join(paragraphs)
    # Clean the text
    cleaned_text = clean_text(text)
    return cleaned_text

# Load the CSV data
df = pd.read_csv('./journal_data.csv')

# Apply text processing to paragraphs
df['cleaned_text'] = df['paragraphs'].apply(process_paragraphs)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(tokenizer=tokenize_text, max_features=1000, token_pattern=None)  # Adjust max_features as needed
tfidf_matrix = vectorizer.fit_transform(df['cleaned_text'])

# Convert TF-IDF matrix to DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# Append the original data with TF-IDF features
df_tfidf = pd.concat([df, tfidf_df], axis=1)

# Save processed data to a new CSV file
df_tfidf.to_csv('./journal_data_processed.csv', index=False)

print("Data processing and saving complete.")
