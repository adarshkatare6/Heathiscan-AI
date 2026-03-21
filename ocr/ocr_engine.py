from __future__ import annotations

from typing import Any

import pytesseract
from PIL import Image, ImageOps

import os
from pathlib import Path


def _configure_tesseract_cmd() -> None:
    """
    Configure pytesseract to point at the Tesseract binary.

    - If `TESSERACT_CMD` is set, use it.
    - Otherwise, try the common Windows install path.
    """
    override = os.getenv("TESSERACT_CMD")
    if override:
        pytesseract.pytesseract.tesseract_cmd = override
        return

    if os.name == "nt":
        default_cmd = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
        if default_cmd.exists():
            pytesseract.pytesseract.tesseract_cmd = str(default_cmd)


# Run on import so OCR works immediately.
_configure_tesseract_cmd()


def _otsu_threshold(gray_img: Image.Image) -> int:
    """
    Compute Otsu threshold without adding heavy dependencies (no numpy).
    Expects a grayscale (mode 'L') image.
    """
    hist = gray_img.histogram()  # length 256
    total = sum(hist)
    if total == 0:
        return 128

    sum_total = sum(i * hist[i] for i in range(256))

    sumB = 0
    wB = 0
    max_var = -1.0
    threshold = 128

    for t in range(256):
        wB += hist[t]
        if wB == 0:
            continue
        wF = total - wB
        if wF == 0:
            break

        sumB += t * hist[t]
        mB = sumB / wB
        mF = (sum_total - sumB) / wF

        # Between-class variance
        var_between = wB * wF * (mB - mF) ** 2
        if var_between > max_var:
            max_var = var_between
            threshold = t

    return int(threshold)


def extract_text(image: Any) -> str:
    """
    Extract text from an image using pytesseract.

    Preprocess:
    - grayscale
    - thresholding (Otsu)

    Returns:
    - extracted text as a string
    """
    if image is None:
        raise ValueError("No image provided for OCR.")

    if not isinstance(image, Image.Image):
        raise TypeError(f"Expected a PIL Image, got: {type(image)}")

    try:
        gray = ImageOps.grayscale(image)
        threshold = _otsu_threshold(gray)
        binary = gray.point(lambda x: 255 if x > threshold else 0)

        # PSM 6 assumes a block of text; works reasonably for ingredient lists.
        text = pytesseract.image_to_string(binary, config="--psm 6")
        return (text or "").strip()
    except Exception as e:
        raise RuntimeError(f"OCR extraction failed: {e}") from e

