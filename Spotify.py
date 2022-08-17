import spotipy
import Keys
from spotipy.oauth2 import SpotifyClientCredentials


def getSpotifyPlaylist():
#Gets songs from a spotify playlist
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=Keys.client_id, client_secret=Keys.client_secret))
    resultsSpotify= Keys.spotifyPlaylist1
    
    return spotify.playlist_tracks(resultsSpotify)