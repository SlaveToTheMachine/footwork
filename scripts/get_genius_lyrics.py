# https://pypi.org/project/lyricsgenius/
# https://lyricsgenius.readthedocs.io/en/master/
import lyricsgenius
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into the environment
token = os.getenv('GENIUS_ACCESS_TOKEN')

genius = lyricsgenius.Genius(token)

# Configure Genius object (optional but recommended)
genius.verbose = False  # Turn off status messages
genius.remove_section_headers = True  # Remove section headers (e.g., [Chorus])
genius.skip_non_songs = True # Skip hits thought to be non-songs

artist_name = "Van Halen"
# A list of top David Lee Roth-era hits to search for specifically
# This list is based on common "top hits" rankings
top_songs = [
    "Jump",
    "Ain't Talkin' 'bout Love",
    "Runnin' with the Devil",
    "Eruption",
    "Panama",
    "Hot for Teacher",
    "Unchained",
    "Dance the Night Away",
    "Jamie's Cryin'",
    "Everybody Wants Some!!",
    "And the Cradle Will Rock...",
    "Mean Street",
    "Beautiful Girls",
    "Somebody Get Me a Doctor",
    "Little Guitars",
    "Romeo Delight",
    "On Fire",
    "Drop Dead Legs",
    "Girl Gone Bad",
    "D.O.A."
]

downloaded_songs = []
for song_title in top_songs:
    print(f"Searching for: {song_title} by {artist_name}")
    try:
        # Search for the specific song and artist
        song = genius.search_song(song_title, artist_name)
        if song:
            downloaded_songs.append(song)
            print(f"Found and added: {song.title}")
            filename = f"../data/lyrics/{song_title.lower().replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                lyrics = song.lyrics
                # path = Path('filename')
                f.write(lyrics)
                print(f"\nSuccessfully saved {song.title} song to {filename}")
        else:
            print(f"Song not found on Genius: {song_title}")
    except Exception as e:
        print(f"An error occurred while searching for {song_title}: {e}")

# Save the lyrics to a single JSON file
if downloaded_songs:
    # Manually create the dictionary for saving, as the built-in save_lyrics() works on an Artist object
    songs_data = {
        "artist": artist_name,
        "songs": [
            {
                "title": s.title,
                "lyrics": s.lyrics,
                "album": s.album,
                "url": s.url
            } for s in downloaded_songs
        ]
    }
    filename = f"../data/lyrics/{artist_name}_top_20_hits.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(songs_data, f, ensure_ascii=False, indent=4)
    print(f"\nSuccessfully saved {len(downloaded_songs)} songs to {filename}")
else:
    print("No songs were successfully downloaded.")
