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
