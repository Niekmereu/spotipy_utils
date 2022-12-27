import spotipy
import random

import spotipy.util as util

PLAYLIST_SHUFFLE_NAME = "Value Snow Days Shuffle"
USERNAME = "11102391517"
PLAYLIST_ID_ORIG = "2lA7j4O7OIMOCcq1C3e0a6"
PLAYLIST_ID_SHUFFLE = "2plQd74hlompIF1g1HzerU"
SCOPE = "playlist-modify-private"

token = util.prompt_for_user_token(USERNAME, scope=SCOPE)
sp = spotipy.Spotify(auth=token)

def get_playlist_tracks(username: str, playlist_id: str):
    # get all tracks belonigng to certain playlist
    
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks



def main():

    # get shuffled tracks and clean shuffled playlist
    playlist_shuffled = get_playlist_tracks(USERNAME, PLAYLIST_ID_SHUFFLE)
    song_ids_shuffled = [song.get("track").get("id") for song in playlist_shuffled]

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

if __name__ == "__main__":
    main()