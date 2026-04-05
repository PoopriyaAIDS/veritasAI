from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import re
import os
import json
import tempfile
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Max upload size: 50MB
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

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

# ─────────────────────────────────────────────
# TESSERACT PATH (for Windows)
# ─────────────────────────────────────────────
try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print("✅ Tesseract OCR ready!")
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False
    print("⚠️  Tesseract not found.")

# ─────────────────────────────────────────────
# TEXT PREPROCESSING
# ─────────────────────────────────────────────
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'^\s*\w[\w\s]*\(reuters\)\s*-\s*', '', text)
    text = re.sub(r'^\s*\w[\w\s]*\(ap\)\s*-\s*',      '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ─────────────────────────────────────────────
# ML MODEL PREDICTION
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# IMAGE → OCR → TEXT
# ─────────────────────────────────────────────
def extract_text_from_image(image_file):
    """Extract text from uploaded image using Tesseract OCR."""
    try:
        from PIL import Image
        import pytesseract

        img  = Image.open(image_file)

        # Convert to RGB if needed
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        # Improve OCR accuracy: resize if too small
        w, h = img.size
        if w < 1000:
            scale = 1000 / w
            img   = img.resize((int(w * scale), int(h * scale)))

        # Extract text
        text = pytesseract.image_to_string(img, lang='eng')
        text = text.strip()

        if len(text) < 20:
            return None, "Could not extract enough text from the image. Please ensure the image contains clear, readable text."

        return text, None

    except Exception as e:
        return None, f"Image processing failed: {str(e)}"

# ─────────────────────────────────────────────
# VIDEO → AUDIO → SPEECH → TEXT
# ─────────────────────────────────────────────
def extract_text_from_video(video_file):
    """Extract speech from uploaded video file using SpeechRecognition."""
    tmp_video = None
    tmp_audio = None

    try:
        import speech_recognition as sr
        from moviepy import VideoFileClip

        # Save uploaded video to temp file
        suffix     = os.path.splitext(video_file.filename)[1] or '.mp4'
        tmp_video  = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        video_file.save(tmp_video.name)
        tmp_video.close()

        # Extract audio from video
        tmp_audio  = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmp_audio.close()

        print(f"Extracting audio from video: {tmp_video.name}")
        clip = VideoFileClip(tmp_video.name)

        if clip.audio is None:
            clip.close()
            return None, "This video has no audio track."

        # Only use first 60 seconds to keep it fast
        duration = min(clip.duration, 60)
        clip     = clip.subclipped(0, duration)
        clip.audio.write_audiofile(tmp_audio.name, fps=16000, logger=None)
        clip.close()

        # Speech to text
        recognizer = sr.Recognizer()
        print("Converting speech to text...")

        with sr.AudioFile(tmp_audio.name) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        if len(text.strip()) < 20:
            return None, "Could not extract enough speech from the video."

        return text.strip(), None

    except sr.UnknownValueError:
        return None, "Could not understand the audio in the video. Please ensure the video has clear speech."
    except sr.RequestError as e:
        return None, f"Speech recognition service error: {str(e)}. Check your internet connection."
    except Exception as e:
        return None, f"Video processing failed: {str(e)}"

    finally:
        # Clean up temp files
        for f in [tmp_video, tmp_audio]:
            if f and os.path.exists(f.name):
                try:
                    os.unlink(f.name)
                except:
                    pass

# ─────────────────────────────────────────────
# HISTORY LOG
# ─────────────────────────────────────────────
HISTORY_FILE = 'analysis_history.json'

def save_to_history(content, result, input_type):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except:
                history = []

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type":      input_type,
        "preview":   content[:120] + "..." if len(content) > 120 else content,
        "verdict":   result.get("verdict"),
        "score":     result.get("credibility_score"),
        "mode":      result.get("analysis_mode")
    }
    history.insert(0, entry)
    history = history[:100]

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "ml_model":  MODEL_LOADED,
        "claude_ai": False,
        "ocr":       OCR_AVAILABLE
    })


@app.route('/analyze', methods=['POST'])
def analyze():
    if not MODEL_LOADED:
        return jsonify({"error": "ML model not loaded. Make sure model.pkl and vectorizer.pkl are present."}), 500

    input_type   = request.form.get('type', 'text')
    content      = request.form.get('content', '').strip()
    extracted_from = None

    try:
        # ── TEXT input ──
        if input_type == 'text':
            if not content or len(content) < 20:
                return jsonify({"error": "Please provide at least 20 characters."}), 400
            analyze_text = content

        # ── IMAGE input ──
        elif input_type == 'image':
            if 'file' not in request.files:
                return jsonify({"error": "No image file uploaded."}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No file selected."}), 400

            allowed = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
            ext     = os.path.splitext(file.filename)[1].lower()
            if ext not in allowed:
                return jsonify({"error": f"Unsupported image format. Use: {', '.join(allowed)}"}), 400

            print(f"Processing image: {file.filename}")
            analyze_text, error = extract_text_from_image(file)
            if error:
                return jsonify({"error": error}), 400

            extracted_from = f"OCR extracted from image: {file.filename}"
            print(f"OCR extracted {len(analyze_text)} characters")

        # ── VIDEO input ──
        elif input_type == 'video':
            if 'file' not in request.files:
                return jsonify({"error": "No video file uploaded."}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No file selected."}), 400

            allowed = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'}
            ext     = os.path.splitext(file.filename)[1].lower()
            if ext not in allowed:
                return jsonify({"error": f"Unsupported video format. Use: {', '.join(allowed)}"}), 400

            print(f"Processing video: {file.filename}")
            analyze_text, error = extract_text_from_video(file)
            if error:
                return jsonify({"error": error}), 400

            extracted_from = f"Speech extracted from video: {file.filename}"
            print(f"Speech-to-text extracted {len(analyze_text)} characters")

        else:
            return jsonify({"error": "Invalid input type."}), 400

        # Run prediction
        result = predict(analyze_text)

        if extracted_from:
            result["extracted_from"] = extracted_from
            result["extracted_text"] = analyze_text[:300] + "..." if len(analyze_text) > 300 else analyze_text

        save_to_history(analyze_text, result, input_type)

        return jsonify({"success": True, "input_type": input_type, "result": result})

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@app.route('/history', methods=['GET'])
def get_history():
    if not os.path.exists(HISTORY_FILE):
        return jsonify([])
    with open(HISTORY_FILE, 'r') as f:
        try:
            return jsonify(json.load(f))
        except:
            return jsonify([])


if __name__ == '__main__':
    print("=" * 50)
    print("  VeritasAI — Fake News Detector")
    print(f"  ML Model : {'✅ Ready' if MODEL_LOADED  else '❌ Not found'}")
    print(f"  OCR      : {'✅ Ready' if OCR_AVAILABLE else '⚠️  Not found'}")
    print("  Open browser at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)