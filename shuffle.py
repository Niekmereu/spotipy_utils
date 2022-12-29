import spotipy
import random
import os
import json

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from spotipy import MemoryCacheHandler

import spotipy.util as util
import streamlit as st

USERNAME = "11102391517"
PLAYLIST_ID_ORIG = "2lA7j4O7OIMOCcq1C3e0a6"
PLAYLIST_ID_SHUFFLE = "2plQd74hlompIF1g1HzerU"
SCOPE = "playlist-modify-private"

load_dotenv()

CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
TOKEN_INFO = os.environ["TOKEN_INFO"]
TOKEN_INFO = eval(TOKEN_INFO)

token = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        show_dialog=False, 
        cache_handler=MemoryCacheHandler(token_info=TOKEN_INFO)
    )


sp = spotipy.Spotify(
    auth_manager=token
)

# token = util.prompt_for_user_token(USERNAME, scope=SCOPE)
# sp = spotipy.Spotify(auth=token)
st.title("Spotify shuffler!")


def get_playlist_tracks(username: str, playlist_id: str):
    """
    Get all tracks belonging to a specific playlist.

    Parameters
    ----------
    username: str
        the id of the user
    playlist_id: str
        the id of the playlist
    """
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def main():

    # get shuffled tracks
    playlist_shuffled = get_playlist_tracks(USERNAME, PLAYLIST_ID_SHUFFLE)
    song_ids_shuffled = [song.get("track").get("id") for song in playlist_shuffled]

    # remove all songs from shuffled playlist
    while song_ids_shuffled:
        results = sp.user_playlist_remove_all_occurrences_of_tracks(
            USERNAME, PLAYLIST_ID_SHUFFLE, song_ids_shuffled[:100]
        )
        song_ids_shuffled = song_ids_shuffled[100:]

    # get original tracks
    playlist_original = get_playlist_tracks(USERNAME, PLAYLIST_ID_ORIG)

    # shuffle them
    random.shuffle(playlist_original)

    # get track IDs
    song_ids = [song.get("track").get("id") for song in playlist_original]

    # insert all tracks to playlist in shuffled order
    while song_ids:
        results = sp.user_playlist_add_tracks(
            USERNAME, PLAYLIST_ID_SHUFFLE, song_ids[:100], position=None
        )
        song_ids = song_ids[100:]


if st.button(
    "Press for shuffle!!",
    help="Press to load songs and insert them into the shuffled playlist",
    on_click=main()
):
    st.write("The spotify playlist was shuffled!")