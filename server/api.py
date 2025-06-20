from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import main  # assumes main.py has download_subtitles
# import card  # assumes card.py has generate_flashcards_from_txt
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, this is fine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/generate-notes")
def generate_notes(youtube_url: str = Form(...)):
    main.download_subtitles(youtube_url)
    # Find the generated notes file
    notes_file = None
    notes = None
    for file in os.listdir('.'):
        if file.endswith('_notes.txt'):
            notes_file = file
            with open(file, 'r', encoding='utf-8') as f:
                notes = f.read()
            break
    if notes_file and notes:
        return {"notes": notes, "notes_file": notes_file}
    return JSONResponse(status_code=404, content={"error": "Notes not found"})

# @app.post("/generate-flashcards")
# def generate_flashcards(notes: str = Form(...)):
#     # Save notes to a temp file
#     temp_file = "temp_notes.txt"
#     with open(temp_file, "w", encoding="utf-8") as f:
#         f.write(notes)
#     flashcards = card.generate_flashcards_from_txt(temp_file)
#     os.remove(temp_file)
#     return {"flashcards": flashcards} 