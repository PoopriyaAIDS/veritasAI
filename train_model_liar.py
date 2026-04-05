import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import os
import re

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_data(filepath):
    # Columns based on LIAR documentation
    # 0: id, 1: label, 2: statement
    df = pd.read_csv(filepath, sep='\t', header=None, usecols=[1, 2], names=['label', 'statement'])
    
    # Map to Binary
    # 'true', 'mostly-true', 'half-true' -> 1 (Real)
    # 'false', 'barely-true', 'pants-fire' -> 0 (Fake)
    binary_mapping = {
        'true': 1, 'mostly-true': 1, 'half-true': 1,
        'false': 0, 'barely-true': 0, 'pants-fire': 0
    }
    df['binary_label'] = df['label'].map(binary_mapping)
    df = df.dropna(subset=['binary_label', 'statement'])
    
    df['cleaned_statement'] = df['statement'].apply(clean_text)
    # Remove extremely short statements
    df = df[df['cleaned_statement'].str.len() > 5]
    
    return df['cleaned_statement'], df['binary_label']

print("Loading LIAR dataset...")
train_dir = 'liar_dataset'
X_train_raw, y_train = load_data(os.path.join(train_dir, 'train.tsv'))
X_test_raw, y_test = load_data(os.path.join(train_dir, 'test.tsv'))

print(f"Training samples: {len(X_train_raw)}")
print(f"Testing samples: {len(X_test_raw)}")

# Vectorize
print("\nVectorizing text...")
vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=20000, 
    ngram_range=(1, 3), # Unigrams, bigrams, trigrams for better context in short text
    min_df=2
)

X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)

# Train
print("\nTraining model...")
model = LogisticRegression(class_weight='balanced', max_iter=1000, C=1.0)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\n=== Model Performance ===")
print(f"Accuracy: {round(accuracy_score(y_test, y_pred) * 100, 2)}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred, target_names=['Fake', 'Real']))

# Save
pickle.dump(model, open("model_liar.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer_liar.pkl", "wb"))
print("\nLIAR Social Media model and vectorizer saved successfully as model_liar.pkl")
