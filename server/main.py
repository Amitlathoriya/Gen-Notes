import os

def generate_notes_from_vtt(vtt_path, video_title=None):
    notes = []
    with open(vtt_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or '-->' in line or line.startswith('WEBVTT') or line.isdigit():
                continue
            notes.append(line)
    # Structure the notes
    structured = []
    if video_title:
        structured.append(f"# {video_title}\n")
    structured.append("## Summary\n")
    # Group lines into paragraphs
    para = []
    for i, line in enumerate(notes):
        para.append(line)
        if len(para) == 4 or i == len(notes) - 1:
            structured.append(f"- {' '.join(para)}\n")
            para = []
    return '\n'.join(structured)

from yt_dlp import YoutubeDL

def download_subtitles(URL):
    # First, extract info to check for available subtitles
    ydl_opts_info = {'skip_download': True}
    with YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(URL, download=False)
        if info is not None:
            subs = info.get('subtitles', {})
            auto_subs = info.get('automatic_captions', {})
        else:
            subs = {}
            auto_subs = {}

    # Try to download regular subtitles first
    if 'en' in subs and subs['en']:
        ydl_opts = {
            'writesubtitles': True,
            'skip_download': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'srt',
            'outtmpl': '%(title)s.%(ext)s',
        }
        print('Downloading regular subtitles...')
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([URL])
    # If no regular subtitles, try auto-generated
    elif 'en' in auto_subs and auto_subs['en']:
        ydl_opts = {
            'writeautomaticsub': True,
            'skip_download': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'srt',
            'outtmpl': '%(title)s.%(ext)s',
        }
        print('No regular subtitles found. Downloading auto-generated subtitles...')
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([URL])
    else:
        print('No subtitles (regular or auto-generated) found for this video.')
        return None

    # Find the downloaded .srt file
    video_title = info.get('title', 'subtitles') if info is not None else 'subtitles'
    srt_filename = f"{video_title}.en.srt"
    if os.path.exists(srt_filename):
        print(f"Subtitles saved as: {srt_filename}")
        notes = generate_notes_from_vtt(srt_filename, video_title)
        notes_filename = f"{video_title}_notes.txt"
        with open(notes_filename, 'w', encoding='utf-8') as f:
            f.write(notes)
        print(f"Notes generated and saved as: {notes_filename}")
    else:
        print("Subtitle file not found after download.")

# Example usage
if __name__ == "__main__":
    URL = input("Enter the YouTube video URL: ")
    download_subtitles(URL)
