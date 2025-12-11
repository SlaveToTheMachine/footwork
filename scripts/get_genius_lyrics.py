# ...existing code...
import lyricsgenius
import json
import os
import re
import csv
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GENIUS_ACCESS_TOKEN")
if not token:
    raise RuntimeError("GENIUS_ACCESS_TOKEN not set in environment")

genius = lyricsgenius.Genius(token)
genius.verbose = False
genius.remove_section_headers = True
genius.skip_non_songs = True

artist_name = "Van Halen"

# Load the list of songs to search from the discography CSV (source of truth)
script_dir = os.path.dirname(__file__)
discog_path = os.path.normpath(os.path.join(script_dir, "..", "data", "van_halen_discography.csv"))
songs_to_search = []
if os.path.exists(discog_path):
    with open(discog_path, newline='', encoding='utf-8') as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            to_search = (row.get('to_search') or '').strip().lower()
            if to_search in ('1', 'true', 'yes', 'y', 't'):
                title = (row.get('song_title') or '').strip()
                if title:
                    songs_to_search.append(title)
else:
    print(f"Warning: discography CSV not found at {discog_path}; no songs loaded")

def slugify(name: str) -> str:
    # replace non-word chars with underscore, collapse multiples
    return re.sub(r'[_]+', '_', re.sub(r'\W+', '_', name)).strip('_').lower()

out_dir = os.path.join("..", "data", "lyrics")
os.makedirs(out_dir, exist_ok=True)

downloaded_songs = []
for song_title in songs_to_search:
    print(f"Searching for: {song_title} by {artist_name}")
    try:
        song = genius.search_song(song_title, artist_name)
        if song:
            downloaded_songs.append(song)
            print(f"Found and added: {song.title}")
            filename = os.path.join(out_dir, f"{slugify(song_title)}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(song.lyrics or "")
            print(f"Saved lyrics to {filename}")
        else:
            print(f"Song not found on Genius: {song_title}")
    except Exception as e:
        print(f"Error while searching {song_title}: {e}")

if downloaded_songs:
    songs_data = {
        "artist": artist_name,
        "songs": [
            {
                "title": s.title,
                "lyrics": s.lyrics,
                "album": getattr(s, "album", None),
                "url": getattr(s, "url", None)
            } for s in downloaded_songs
        ]
    }
    json_path = os.path.join(out_dir, f"{slugify(artist_name)}_top_songs.json")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(songs_data, jf, ensure_ascii=False, indent=4)
    print(f"Saved {len(downloaded_songs)} songs to {json_path}")
else:
    print("No songs were successfully downloaded.")
