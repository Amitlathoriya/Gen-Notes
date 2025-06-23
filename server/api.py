from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp.utils import DownloadError, ExtractorError
import main  # assumes main.py has download_subtitles
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# FastAPI instance
app = FastAPI()

# Allow all CORS origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Gen Notes API!"}

# Notes generation endpoint
@app.post("/generate-notes")
def generate_notes(youtube_url: str = Form(...)):
    logging.info(f"Received request for: {youtube_url}")
    try:
        notes = main.download_subtitles(youtube_url)
        if notes:
            return {"notes": notes}
        logging.warning("Subtitles not found or empty.")
        return JSONResponse(status_code=404, content={"error": "Could not find subtitles for this video."})
    except (DownloadError, ExtractorError) as e:
        logging.error(f"Download/Extraction Error: {e}")
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        logging.exception("Unexpected error during subtitle generation.")
        return JSONResponse(status_code=500, content={"error": "An unexpected server error occurred."})
