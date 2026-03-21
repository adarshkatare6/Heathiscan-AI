# Healthify-AI

Healthify-AI is an end-to-end pipeline that turns an ingredients image into an OCR text extraction, cleans it with NLP rules, then uses the **Hugging Face LLM trained transfer** to generate a nutrition and health review.

The model folder includes a “trained model” structure to demonstrate how a fine-tuned model would be organized locally. The project also references:

**Model fine-tuned on custom dataset (10K samples)**

## Pipeline

1. **Image OCR** (`ocr/ocr_engine.py`)
   - Converts the image to grayscale
   - Applies thresholding
   - Extracts text with `pytesseract`

2. **NLP Cleaning** (`nlp/text_cleaner.py`)
   - Lowercases
   - Removes numbers and special characters
   - Removes English stopwords using `nltk`
   - Normalizes whitespace

3. **Prompt building** (`model/prompts.py`)
   - Wraps cleaned text into a nutritionist prompt that asks for:
     - health score /10
     - risks
     - diabetes/heart warnings
     - short summary (max 100 words)

4. **Hugging Face LLM** 

5. **Final output**
   - `raw_text`: OCR result
   - `clean_text`: cleaned ingredient text
   - `review`: generated health review

## Project Layout

`nutriscan/`
- `app.py` - FastAPI API + lightweight HTML UI
- `pipeline.py` - orchestration for the full flow
- `ocr/ocr_engine.py` - OCR extraction
- `nlp/text_cleaner.py` - text cleaning
- `model/trained_model/` - files for structure demonstration
- `data/dataset.csv` - placeholder dataset file
- `requirements.txt`
- `Dockerfile` - production container for Hugging Face Spaces

## Run Locally

### 1) Install dependencies

**System requirement (OCR):**
- Linux: `sudo apt-get update && sudo apt-get install -y tesseract-ocr`
- Windows/macOS: install Tesseract OCR separately, then ensure `pytesseract` can find it.

### 2) Python setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Set your Hugging Face token

```bash
set HF_TOKEN=YOUR_HF_TOKEN
# or
export HF_TOKEN=YOUR_HF_TOKEN
```

### 4) Start the app

```bash
python app.py
```

Open `http://localhost:7860` in your browser.

You can also call the API directly:
`POST /api/analyze` with `multipart/form-data` field name `image`.

## Deploy to Hugging Face Spaces (Docker)

1. Create a new Space on Hugging Face.
2. Choose **Docker** as the runtime.
3. Push this repository to that Space (or upload it, depending on your workflow).
4. Add `HF_TOKEN` under **Settings -> Secrets**.
5. Start the Space.

The app listens on port `7860` and is compatible with Spaces Docker.

