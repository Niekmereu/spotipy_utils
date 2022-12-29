# Spotify Utils

## How to set up the environment

The environment is set up with Conda:

```
conda env create -f environment.yml
```
And then activated:
```
conda activate <env_name>
```
## Spotify develoloper account

A spotify developer account is needed. Click [here](https://developer.spotify.com/dashboard/login) for instructions. The credentials of this developer account should be storeed in the environment variables.


## Environment variables

Creeate a .env file in the project root with the following environment variables:

```
SPOTIPY_CLIENT_ID=<SPOTIFY_CLIENT_ID>
SPOTIPY_CLIENT_SECRET=<SPOTIFY_CLIENT_ID>
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'
```

The spotify redirect uri is used for authentication purposes. 

## Tools

### Shuffle
Extract tracks from a given playlist and store them shuffled in a second playlist. Parameters are hard coded in `shuffle.py`.

For music shuffling run from the root:

```
python shuffle.py
```