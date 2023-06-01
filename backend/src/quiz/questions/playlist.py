import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

# Set up authentication
client_id = 'N/A'
client_secret = 'N/A'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_song(artist, track):
    results = sp.search(q=f"artist:{artist} track:{track}", type='track', limit=1)
    items = results['tracks']['items']
    if items:
        return items[0]['uri']
    else:
        return None

def create_playlist(artist_song_list):
    # Create an empty collaborative playlist
    headers = {
        'Authorization': f'Bearer {client_credentials_manager.get_access_token()}',
        'Content-Type': 'application/json'
    }
    data = {
        'name': 'My Playlist',
        'collaborative': True,
        'public': True,
        'description': 'My custom playlist'
    }
    response = requests.post('https://api.spotify.com/v1/playlists', headers=headers, data=json.dumps(data))
    
    if response.status_code != 201:
        print(response.content)  # Print the response content for troubleshooting
        raise ValueError('Failed to create playlist. Please check your request.')
    
    playlist = response.json()
    playlist_id = playlist['id']
    playlist_url = playlist['external_urls']['spotify']

    # Iterate over the artist-song list and add each song to the playlist
    for artist, song in artist_song_list:
        uri = search_song(artist, song)
        if uri:
            sp.playlist_add_items(playlist_id=playlist_id, items=[uri])

    return playlist_url

artist_song_list = [('Artist 1', 'Song 1'), ('Artist 2', 'Song 2'), ('Artist 3', 'Song 3')]
playlist_url = create_playlist(artist_song_list)
print("Playlist created:", playlist_url)