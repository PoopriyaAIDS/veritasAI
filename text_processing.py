import pickle
import re

# ─────────────────────────────────────────────
# LOAD YOUR TRAINED MODEL & VECTORIZER
# ─────────────────────────────────────────────
print("Loading your trained model...")
try:
    model      = pickle.load(open("model.pkl",      "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    print("✅ Model and vectorizer loaded successfully!")
    MODEL_LOADED = True
except Exception as e:
    print(f"❌ Could not load model: {e}")
    MODEL_LOADED = False

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'^\s*\w[\w\s]*\(reuters\)\s*-\s*', '', text)
    text = re.sub(r'^\s*\w[\w\s]*\(ap\)\s*-\s*',      '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def predict(text):
    cleaned    = clean_text(text)
    vectorized = vectorizer.transform([cleaned])

    prediction    = model.predict(vectorized)[0]
    probabilities = model.predict_proba(vectorized)[0]

    fake_prob = round(probabilities[0] * 100, 1)
    real_prob = round(probabilities[1] * 100, 1)

    verdict        = "REAL NEWS" if prediction == 1 else "FAKE NEWS"
    confidence_pct = real_prob   if prediction == 1 else fake_prob

    if confidence_pct >= 85:
        confidence = "HIGH"
    elif confidence_pct >= 65:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    credibility_score = int(real_prob)

    # Reasoning
    if verdict == "REAL NEWS":
        if confidence == "HIGH":
            reasoning = f"The ML model analyzed the text using TF-IDF features and Logistic Regression. The content shows strong indicators of credible journalism with {real_prob}% real probability. The writing style, vocabulary, and structure are consistent with factual reporting."
        elif confidence == "MEDIUM":
            reasoning = f"The model detected moderately credible patterns in the text ({real_prob}% real probability). The content appears to follow journalistic conventions but some uncertainty remains. Consider verifying key claims with additional sources."
        else:
            reasoning = f"The model leans toward real news ({real_prob}% real probability) but with low confidence. The text has some credible patterns but also ambiguous signals. Manual verification is strongly recommended."
    else:
        if confidence == "HIGH":
            reasoning = f"The ML model detected strong fake news indicators ({fake_prob}% fake probability). The text contains patterns commonly associated with misinformation such as sensational language, unverified claims, and emotional manipulation techniques."
        elif confidence == "MEDIUM":
            reasoning = f"The model found moderate fake news signals ({fake_prob}% fake probability). The content shows some suspicious patterns including potentially unverified claims. Cross-check this information with trusted news sources before sharing."
        else:
            reasoning = f"The model leans toward fake news ({fake_prob}% fake probability) but with low confidence. The content has mixed signals — some parts seem credible while others raise concerns. Independent verification is recommended."

    # Red flags
    red_flags  = []
    text_lower = text.lower()
    if any(w in text_lower for w in ['share', 'before it gets deleted', 'before they delete']):
        red_flags.append("Urgency to share before deletion — common manipulation tactic")
    if any(w in text_lower for w in ['bombshell', 'shocking', 'breaking', 'exposed', 'horrified']):
        red_flags.append("Sensational headline language designed to provoke emotion")
    if any(w in text_lower for w in ['anonymous', 'whistleblower', 'insider', 'secret source']):
        red_flags.append("Relies on anonymous or unverified sources")
    if any(w in text_lower for w in ['deep state', 'globalist', 'new world order', 'cabal']):
        red_flags.append("Conspiracy theory terminology detected")
    if any(w in text_lower for w in ['big pharma', 'they dont want you', 'hidden cure', 'banned']):
        red_flags.append("Anti-establishment health misinformation pattern")
    if any(w in text_lower for w in ['wake up', 'sheeple', 'sheep', 'blind']):
        red_flags.append("Condescending language targeting the reader")
    if text.count('!') >= 3:
        red_flags.append("Excessive exclamation marks — emotional manipulation indicator")
    if any(w in text_lower for w in ['100%', 'guaranteed', 'proven', 'definitive proof']):
        red_flags.append("Overconfident absolute claims without evidence")
    if any(w in text_lower for w in ['microchip', '5g', 'chemtrail', 'flat earth']):
        red_flags.append("Known conspiracy theory topic detected")

    # Tip
    if verdict == "FAKE NEWS":
        tip = "Cross-check this story on Reuters, AP News, BBC, or other established outlets. If you cannot find it reported elsewhere, it is likely false."
    elif confidence == "LOW":
        tip = "While this appears real, the confidence is low. Verify the key claims on trusted fact-checking sites like Snopes, FactCheck.org, or PolitiFact."
    else:
        tip = "Even credible-looking news can be misleading. Always check the original source and look for corroborating reports from multiple outlets."

    return {
        "verdict":           verdict,
        "confidence":        confidence,
        "confidence_pct":    confidence_pct,
        "credibility_score": credibility_score,
        "real_probability":  real_prob,
        "fake_probability":  fake_prob,
        "reasoning":         reasoning,
        "red_flags":         red_flags,
        "tips":              tip,
        "ml_score":          credibility_score,
        "ml_verdict":        verdict,
        "ml_confidence_pct": confidence_pct,
        "claude_verdict":    "N/A",
        "claude_score":      None,
        "analysis_mode":     "ML Model (Logistic Regression + TF-IDF)"
    }
