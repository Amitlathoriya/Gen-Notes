from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import main  # assumes main.py has download_subtitles
# import card  # assumes card.py has generate_flashcards_from_txt
import os
from yt_dlp.utils import DownloadError

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, this is fine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gen Notes API!"}

@app.post("/generate-notes")
def generate_notes(youtube_url: str = Form(...)):
    try:
        notes = main.download_subtitles(youtube_url)
        if notes:
            return {"notes": notes}
        # This will now handle cases where subtitles are not found
        return JSONResponse(status_code=404, content={"error": "Could not find subtitles for this video."})
    except DownloadError as e:
        # This will catch errors like "Video unavailable"
        return JSONResponse(status_code=400, content={"error": "Video is unavailable or region-locked."})
    except Exception as e:
        # Catch any other unexpected errors
        return JSONResponse(status_code=500, content={"error": "An unexpected error occurred."})

# @app.post("/generate-flashcards")
# def generate_flashcards(notes: str = Form(...)):
#     # Save notes to a temp file
#     temp_file = "temp_notes.txt"
#     with open(temp_file, "w", encoding="utf-8") as f:
#         f.write(notes)
#     flashcards = card.generate_flashcards_from_txt(temp_file)
#     os.remove(temp_file)
#     return {"flashcards": flashcards} 
