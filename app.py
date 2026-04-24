from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Max upload size: 50MB
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# IMPORTS FROM MODULES
# ─────────────────────────────────────────────
from text_processing import predict, MODEL_LOADED
from image_processing import extract_text_from_image, OCR_AVAILABLE
from video_processing import extract_text_from_video

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