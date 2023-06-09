import requests
from bs4 import BeautifulSoup

url = 'https://music.apple.com/ca/playlist/nails/pl.u-38oW9qetPWme7qY'

# Send a GET request to the playlist URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the song names
song_names = []
song_elements = soup.select('.songs-list-row__song-name')
for element in song_elements:
    song_names.append(element.text.strip())

album_names = []
div_element = soup.find_all('div', attrs={'class': 'songs-list__col songs-list__col--tertiary svelte-17mxcgw', 'data-testid': 'track-column-tertiary'})
for element in div_element:
    album_names.append(element.text.strip())

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIFY_CLIENT_ID = '750304b8715e410988718890a8a3ad0a'
SPOTIFY_CLIENT_SECRET = 'ca371592f31645629a73e5054b4e7bfa'
SPOTIFY_REDIRECT_URI = 'https://open.spotify.com/'
SCOPE = 'playlist-modify-public'

# Authenticate with Spotify

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope=SCOPE))# Get the user's ID
user_id = sp.me()['id']


# Create a new playlist
playlist_name = 'Nails'
playlist_description = 'This is a playlist created using Python'
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)

# Search and add songs to the playlist
for song, album in zip(song_names, album_names):
    query = f"track:{song} album:{album}"
    search_results = sp.search(q=query, type='track', limit=1)
    if search_results['tracks']['items']:
        track_uri = search_results['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist_id=playlist['id'], items=[track_uri])

# Print the URL of the created playlist
print("Playlist created successfully.")
print(f"Playlist URL: {playlist['external_urls']['spotify']}")
