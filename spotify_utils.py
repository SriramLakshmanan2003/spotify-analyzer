import spotipy 
import streamlit as st

sp=spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(client_id=st.secrets["SPOTIFY_CLIENT_ID"], client_secret=st.secrets["SPOTIFY_CLIENT_SECRET"]))


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