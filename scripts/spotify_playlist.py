import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# 1. Authenticate
load_dotenv()
YOUR_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
YOUR_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUR_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=YOUR_CLIENT_ID,
    client_secret=YOUR_CLIENT_SECRET,
    redirect_uri=YOUR_REDIRECT_URI,
    # redirect_uri="http://localhost:8080/callback",
    scope="playlist-modify-public playlist-modify-private"
))

# 2. Provide your list of songs
songs = [
    "Back in Black AC/DC",
    "Bad Guy Billie Eilish",
    "Lose Yourself Eminem",
    "Panama Van Halen",
    "Ain't Talkin' 'Bout Love Van Halen",
]

# 3. Search each song → Get the track ID
track_ids = []

for title in songs:
    results = sp.search(q=title, limit=1, type='track')
    items = results['tracks']['items']
    if items:
        track_ids.append(items[0]['id'])
    else:
        print(f"Not found: {title}")
        
# 4. Create a playlist
user_id = sp.current_user()["id"]

playlist = sp.user_playlist_create(
    user=user_id,
    name="My Programmatic Playlist",
    public=False,
    description="Generated from a Python script"
)

playlist_id = playlist['id']

# 5. Add tracks to the playlist
sp.playlist_add_items(playlist_id, track_ids)
print("Playlist created!")