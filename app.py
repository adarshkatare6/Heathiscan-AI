from __future__ import annotations

import io
from typing import Any, Dict

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image

from pipeline import run_pipeline

app = FastAPI(title="NutriScan API")


@app.get("/")
def index() -> FileResponse:
    # Serves a small static UI (no gradio).
    return FileResponse("index.html", media_type="text/html")


@app.get("/script.js")
def script_js() -> FileResponse:
    return FileResponse("script.js", media_type="application/javascript")


@app.get("/style.css")
def style_css() -> FileResponse:
    return FileResponse("style.css", media_type="text/css")


@app.post("/api/analyze")
async def analyze(image: UploadFile = File(...)) -> JSONResponse:
    """
    Analyze an uploaded ingredient image.

    Returns:
      {
        "raw_text": ...,
        "clean_text": ...,
        "review": ...
      }
    """
    if not image:
        raise HTTPException(status_code=400, detail="Missing uploaded image.")

    if image.content_type and not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type: {image.content_type}. Expected an image.",
        )

    try:
        contents = await image.read()
        if not contents:
            raise ValueError("Empty upload.")

        pil_image = Image.open(io.BytesIO(contents))
        pil_image.load()  # Ensure the image is fully decoded.
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image upload: {e}")

    try:
        result: Dict[str, Any] = run_pipeline(pil_image)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return JSONResponse(content=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7860)

