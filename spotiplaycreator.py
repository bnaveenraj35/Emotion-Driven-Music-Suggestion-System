import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Set up your Spotify application credentials
CLIENT_ID = 'e258cbfa84374846ab13c566c7f5df21'
CLIENT_SECRET = 'fce26c3e38d04bf4a91f4bf60add3f47'
REDIRECT_URI = 'http://localhost:5000/callback'  # Set this redirect URI in your Spotify Developer Dashboard

# Authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='playlist-modify-public'))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='playlist-modify-public',
                                               username='31kih37uliem2cefyfckku4xtcpe'))

def create_playlist(name):
    playlist = sp.user_playlist_create(sp.me()['id'], name, public=True)
    return playlist['id']

def delete_playlist(playlist_id):
    sp.user_playlist_unfollow(sp.me()['id'], playlist_id)

def get_playlist_id_by_name(name):
    playlists = sp.user_playlists(sp.me()['id'])
    for playlist in playlists['items']:
        if playlist['name'] == name:
            return playlist['id']
    return None
def add_song_to_playlist(playlist_id, track_uris):
    sp.playlist_add_items(playlist_id, track_uris)
    print("Songs added to the playlist successfully!")

def search_track(song_name):
    results = sp.search(q=song_name, limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        return track_uri
    else:
        print("No track found for the given song name.")
        return None


def create_playlist_and_add_songs(emotion):
    print(emotion+"Inside spotify function")
    # Remove existing playlist for the given emotion
    existing_playlist_id = get_playlist_id_by_name(f"{emotion.capitalize()} Playlist")
    print(existing_playlist_id)
    if existing_playlist_id:
        delete_playlist(existing_playlist_id)
        print(f"Existing '{emotion.capitalize()} Playlist' deleted successfully!")

    # Read CSV file containing song names
    with open("stored_songs.csv", "r") as csvfile:
        songs = csvfile.readlines()

    # Remove newline characters
    songs = [song.strip() for song in songs]

    # Create the new playlist
    playlist_name = f"{emotion.capitalize()} Playlist"
    playlist_id = create_playlist(playlist_name)
    print(f"New '{emotion.capitalize()} Playlist' created successfully!")

    # Add songs to the playlist
    track_uris = [search_track(song) for song in songs]
    track_uris = [uri for uri in track_uris if uri is not None]
    if track_uris:
        add_song_to_playlist(playlist_id, track_uris)

#create_playlist_and_add_songs("happy")
  # Example usage
