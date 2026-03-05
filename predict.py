import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# Load trained model & vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Preprocessing
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
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
    print("Real News ✅")
else:
    print("Fake News ❌")