import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import pandas as pd
import webbrowser

def classify_songs(artist_name, recognized_emotion):
    print(recognized_emotion)
    client_id = "e258cbfa84374846ab13c566c7f5df21"
    client_secret = "fce26c3e38d04bf4a91f4bf60add3f47"
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

    # Search for the artist
    results = sp.search(q=artist_name, type="artist", limit=1)

    # Get the artist ID
    if "artists" in results and "items" in results["artists"]:
        artist = results["artists"]["items"][0]
        artist_id = artist["id"]
        print(f"Artist: {artist_name}, ID: {artist_id}")
    else:
        print(f"Artist '{artist_name}' not found.")

    AUTH_URL = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'
    # extract all albums
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', 
                     headers=headers, 
                     params={'include_groups': 'album', 'limit': 5})
    d = r.json()

    trackinfo = []   # will hold all track info
    albums = [] # to keep track of duplicates

    # loop over albums and get all tracks
    print("Album")
    for album in d['items']:
        album_name = album['name']

        # here's a hacky way to skip over albums we've already grabbed
        trim_name = album_name.split('(')[0].strip()
        if trim_name.upper() in albums:
            continue
        albums.append(trim_name.upper()) # use upper() to standardize

        # this takes a few seconds so let's keep track of progress    
        print(album_name)

        # pull all tracks from this album
        r = requests.get(BASE_URL + 'albums/' + album['id'] + '/tracks', 
            headers=headers)
        tracks = r.json()['items']

        for track in tracks:
            # get track information
            f = requests.get(BASE_URL + 'tracks/' + track['id'], 
                headers=headers)
            f = f.json()

         # combine with album info
            f.update({
                'album_name': album_name,
                'release_date': album['release_date'],
                'album_id': album['id']
            })

            trackinfo.append(f)
    # Load all the extracted data into a dataframe and preview dataframe.
    df = pd.DataFrame(trackinfo)

    audiofeature = []   # will hold all audio feature info
    albums = [] # to keep track of duplicates

    # loop over albums and get all tracks
    for album in d['items']:
        album_name = album['name']

        # here's a hacky way to skip over albums we've already grabbed
        trim_name = album_name.split('(')[0].strip()
        if trim_name.upper() in albums:
            continue
        albums.append(trim_name.upper()) # use upper() to standardize

        # this takes a few seconds so let's keep track of progress    
        print(album_name)

        # pull all tracks from this album
        r = requests.get(BASE_URL + 'albums/' + album['id'] + '/tracks', 
            headers=headers)
        tracks = r.json()['items']

        for track in tracks:
            # get audio features (key, liveness, danceability, ...)
            f = requests.get(BASE_URL + 'audio-features/' + track['id'], 
                headers=headers)
            f = f.json()

            # combine with album info
            f.update({
                'track_name': track['name'],
                'album_name': album_name,
                'release_date': album['release_date'],
                'album_id': album['id']
            })

            audiofeature.append(f)
    # Load all the extracted data into a dataframe and preview dataframe.
    df1 = pd.DataFrame(audiofeature)
    df.isna().sum()

    df = df[['album_id','album_name', 'id', 'name']]
    df.duplicated().sum()

    df1.isna().sum()
    df1 = df1[['album_id','album_name', 'id', 'track_name', 'energy', 'valence']]
    df1.head()
    df1.duplicated().sum()
    df1.shape
    df.shape
    df1=df1.drop(['album_id','album_name', 'id', 'track_name'],axis=1)
    df1
    df2 = pd.concat([df, df1], axis=1)
    df2

    df2.duplicated().sum()
    df2.isna().sum()
    df2['url'] = "https://open.spotify.com/track/"+df2['id']
    df2

    # Export as CSV file.
    df2.to_csv("thefinalsongs.csv", sep = ',')

    #example
    info = []  # Array of arrays to store track names and URLs
    filtered_tracks = []
    for _, row in df2.iterrows():
        track_name = row["name"]
        valence = row["valence"]
        arousal = row["energy"]  
        url = row["url"]

        if recognized_emotion == "happy":
            if 0.5 <= valence <= 1.0 and 0.5 <=  arousal <= 1.0:
                filtered_tracks.append((track_name,url))
                info.append([track_name,url])
                print(track_name)
        elif recognized_emotion == "calm":
            if 0.5 <= valence <= 1.0 and 0.0 <=  arousal <= 0.5:
                filtered_tracks.append((track_name,url))
                info.append([track_name,url])
                print(track_name)
        elif recognized_emotion == "sad":
            if 0.0 <= valence <= 0.5 and 0.0 <=  arousal <= 0.5:
                filtered_tracks.append((track_name,url))
                info.append([track_name,url])
                print(track_name)
        elif recognized_emotion == "anger":
            if 0.0 <= valence <= 0.5 and 0.5 <=  arousal <= 1.0:
                filtered_tracks.append((track_name,url))
                info.append([track_name,url])
                print(track_name)
    import csv

    # Open the CSV file in append mode
    with open('stored_songs.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writerow(['Track Name', 'Track URL'])

        # Write each selected track to the CSV file
        for track, track_url in filtered_tracks:
            writer.writerow([track, track_url])
    
    print("Information is returned")
    print(info)
    return info
#classify_songs("Charlie Puth", "sad")
