from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Text preprocessing
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    news = request.form['news']
    news_clean = clean_text(news)
    news_vector = vectorizer.transform([news_clean])
    prediction = model.predict(news_vector)[0]
    if prediction == 1:
        result = "Real News ✅"
    else:
        result = "Fake News ❌"
    return render_template('index.html', prediction=result, news=news)

if __name__ == '__main__':
    app.run(debug=True)