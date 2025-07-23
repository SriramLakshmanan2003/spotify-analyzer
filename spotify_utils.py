import spotipy 
import re

sp=spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(client_id='92dd80c97bef40dcb35f7ef6f3c3c33c', client_secret='2d76e0dbc67e4dbfb3d5271cb79913c4'))


def extract_track_data(url):
    track_id = url.split("track/")[-1].split("?")[0]
    track = sp.track(track_id)
    return {
        'track_id': track['id'],
        'track_name': track['name'],
        'artist_name': track['artists'][0]['name'],
        'album_name': track['album']['name'],
        'release_date': track['album']['release_date'],
        'duration_min': round(track['duration_ms'] / 60000, 2),
        'popularity': track['popularity'],
        'spotify_url': url
    }