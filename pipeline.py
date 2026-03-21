from typing import Any, Dict

from nlp.text_cleaner import clean_text as clean_text_fn
from model.inference import generate_review
from model.prompts import build_prompt
from ocr.ocr_engine import extract_text


def run_pipeline(image: Any) -> Dict[str, str]:
    """
    End-to-end pipeline:
    Image -> OCR -> NLP Cleaning -> HuggingFace Inference -> Health Review Output
    """
    raw_text = extract_text(image)
    clean_text = clean_text_fn(raw_text)
    prompt = build_prompt(clean_text)
    review = generate_review(prompt)

    return {
        "raw_text": raw_text,
        "clean_text": clean_text,
        "review": review,
    }

