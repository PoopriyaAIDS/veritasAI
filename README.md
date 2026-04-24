# VeritasAI — AI-Based Fake News Detection System

> *Veritas* (Latin) = **Truth** | AI = **Artificial Intelligence**  
> **The Truth Engine — Powered by Machine Learning**

---

## 📌 About
VeritasAI is an AI-based fake news detection web application that 
classifies news as REAL or FAKE with **91.34% accuracy** across 
8 news categories using Machine Learning and NLP techniques.

---

## ✨ Features
- 📝 **Text Input** — Paste any news article or headline
- 🖼️ **Image Input** — Upload screenshot (OCR text extraction)
- 🎬 **Video Input** — Upload video (Speech-to-Text extraction)
- 📊 **Credibility Score** — 0 to 100 trustworthiness rating
- 🚩 **Red Flag Detection** — 9 misinformation patterns
- 💬 **Chatbot Assistant** — Rule-based FAQ bot
- 🗂️ **Analysis History** — Saves all past analyses

---

## 🧠 AI Techniques Used
| Technique | Purpose |
|-----------|---------|
| Logistic Regression | Core ML classification |
| TF-IDF Vectorization | Convert text to numerical features |
| N-gram Analysis (1,2) | Capture word pairs for context |
| NLP Preprocessing | Clean and normalize text |
| Tesseract OCR | Extract text from images |
| Speech-to-Text | Extract speech from videos |

---

## 🛠️ Tech Stack
**Backend:** Python, Flask, Scikit-learn, Pandas, NumPy  
**Frontend:** HTML5, CSS3, JavaScript  
**ML/NLP:** Logistic Regression, TF-IDF, N-grams  
**Image:** Tesseract OCR, Pytesseract, Pillow  
**Video:** MoviePy, SpeechRecognition, PyDub  

---

## 📊 Model Performance
| Metric | Value |
|--------|-------|
| Accuracy | 91.34% |
| Training Articles | 200,000+ |
| News Categories | 8 |
| Dataset Coverage | 2010–2022 |

---

## 📁 Datasets Used
| Dataset | Articles | Coverage |
|---------|----------|----------|
| ISOT Dataset | 117,033 | 2010–2017 |
| WELFake Dataset | 72,134 | Up to 2022 |
| LIAR Dataset | 12,791 | Up to 2022 |

---

## 📰 Supported News Categories
🏛️ Politics · 🏥 Health · 🔭 Science · 💰 Business  
⚽ Sports · 🎬 Entertainment · 🌍 Environment · 🚔 Crime

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x
- Tesseract OCR installed

### Steps
```bash
# Clone the repository
git clone https://github.com/PoopriyaAIDS/veritasAI.git

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser
http://localhost:5000
```

---

## 👩‍💻 Developer
**Poopriya P** — AI & Data Science Student
