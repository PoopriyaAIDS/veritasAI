import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# Load trained model & vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Preprocessing
def clean_text(text):
    text = str(text).lower()
    
    # SAFE dateline removal - only removes "city (source) - " patterns
    text = re.sub(r'^\s*[a-z\s]+\([a-z]+\)\s*-\s*', '', text)
    text = re.sub(r'^\s*[a-z\s]{3,20}\s+-\s+', '', text)
    
    # Date patterns remove
    text = re.sub(r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b', '', text)
    text = re.sub(r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b', '', text)
    
    # Year remove
    text = re.sub(r'\b(19|20)\d{2}\b', '', text)
    
    # Special characters remove
    text = re.sub(r'[^a-z\s\-]', '', text)
    text = re.sub(r'\s-\s', ' ', text)
    text = re.sub(r'^-+', '', text)
    
    # Extra spaces clean
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Input from user
news = input("Enter news text: ")
news_clean = clean_text(news)

# Vectorize & predict
news_vector = vectorizer.transform([news_clean])
prediction = model.predict(news_vector)[0]

# Show result
if prediction == 1:
    print("Real News")
else:
    print("Fake News")