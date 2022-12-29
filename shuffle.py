import streamlit as st
import pandas as pd
import numpy as np
import spotipy
import random

from dotenv import load_dotenv

import spotipy.util as util

USERNAME = "11102391517"
PLAYLIST_ID_ORIG = "2lA7j4O7OIMOCcq1C3e0a6"
PLAYLIST_ID_SHUFFLE = "2plQd74hlompIF1g1HzerU"
SCOPE = "playlist-modify-private"

load_dotenv()

token = util.prompt_for_user_token(USERNAME, scope=SCOPE)
sp = spotipy.Spotify(auth=token)
st.title("Shuffle our playlist!")

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



st.button("shuffle", on_click=main())