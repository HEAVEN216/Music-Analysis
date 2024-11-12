import requests
import base64
import pandas as pd


# Spotify authorization (Client Credentials flow)
def get_spotify_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_header}"}
    payload = {"grant_type": "client_credentials"}
    
    response = requests.post(auth_url, headers=headers, data=payload)
    response.raise_for_status()  # Ensure successful request
    
    return response.json().get("access_token")


# Fetch Spotify's top tracks from a specific playlist (handles pagination)
def get_spotify_top_tracks(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    
    tracks = []
    
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure successful request
        data = response.json()
        
        # Add the current page of tracks to the list
        tracks.extend(data['items'])
        
        # Check if there's another page
        url = data.get('next')
    
    return {'items': tracks}

# Extract all relevant track information from the playlist data
def extract_all_tracks_to_df(top_tracks_data):
    tracks = top_tracks_data['items']
    track_data = []
    
    for item in tracks:
        track_info = item['track']
        track_name = track_info['name']
        
        # Handle missing artist names safely, making sure there are no None values
        artist_names = [artist.get('name') for artist in track_info['artists']]
        artist_names = [name if name is not None else 'Unknown Artist' for name in artist_names]
        artist_name = ", ".join(artist_names)
        
        track_uri = track_info['uri']
        popularity = track_info['popularity']
        album_name = track_info['album']['name']
        album_uri = track_info['album']['uri']
        release_date = track_info['album']['release_date']
        duration_ms = track_info['duration_ms']
        
        track_data.append({
            'Track Name': track_name,
            'Artists': artist_name,
            'Track URI': track_uri,
            'Popularity': popularity,
            'Album Name': album_name,
            'Album URI': album_uri,
            'Release Date': release_date,
            'Duration (ms)': duration_ms
        })
    
    # Create DataFrame
    df = pd.DataFrame(track_data)
    return df


# Fetch album details from Spotify using the album_id
def get_album_details(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure successful request
    
    return response.json()

# Modify the extract_all_tracks_to_df function to also fetch album details
def extract_album_details_to_df(album_details):
    # Extract relevant fields from the album_details JSON
    album_data = {
        'Album Name': album_details.get('name', 'Unknown Album'),
        'Album URI': album_details.get('uri', 'Unknown URI'),
        'Release Date': album_details.get('release_date', 'Unknown Release Date'),
        'Total Tracks': album_details.get('total_tracks', 'Unknown Total Tracks'),
        'Album Type': album_details.get('type', 'Unknown Type'),
        'Genres': album_details.get('genres', 'Unknown Genres'),
        'Artists': ", ".join([artist['name'] for artist in album_details.get('artists', [])]),
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([album_data])
    return df

def get_spotify_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    
    tracks = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure successful request
        data = response.json()
        
        # Add the current page of tracks to the list
        tracks.extend(data['items'])
        
        # Check if there's another page
        url = data.get('next')
    
    return tracks

# Extract album and track details into a DataFrame
def extract_album_and_tracks_to_df(album_details, tracks):
    album_info = {
        'Album Name': album_details.get('name', 'Unknown Album'),
        'Album URI': album_details.get('uri', 'Unknown URI'),
        'Release Date': album_details.get('release_date', 'Unknown Release Date'),
        'Total Tracks': album_details.get('total_tracks', 'Unknown Total Tracks'),
        'Album Type': album_details.get('type', 'Unknown Type'),
        'Genres': ", ".join(album_details.get('genres', [])),
        'Artists': ", ".join([artist['name'] for artist in album_details.get('artists', [])]),
    }
    
    # Create a list to store all the track data
    track_data = []
    
    # Loop through each track and combine with album info
    for track in tracks:
        track_info = track['track']
        track_data.append({
            'Track Name': track_info.get('name', 'Unknown Track'),
            'Track URI': track_info.get('uri', 'Unknown URI'),
            'Popularity': track_info.get('popularity', 'Unknown Popularity'),
            'Duration (ms)': track_info.get('duration_ms', 'Unknown Duration'),
            'Track Number': track_info.get('track_number', 'Unknown Track Number'),
            'Album Name': album_info['Album Name'],
            'Album URI': album_info['Album URI'],
            'Release Date': album_info['Release Date'],
            'Artists': album_info['Artists'],
            'Genres': album_info['Genres'],
        })
    
    # Convert track data to DataFrame
    df = pd.DataFrame(track_data)
    return df


def get_spotify_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    
    tracks = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure successful request
        data = response.json()
        
        # Add the current page of tracks to the list
        tracks.extend(data['items'])
        
        # Check if there's another page
        url = data.get('next')
    
    return tracks

# Extract album and track details into a DataFrame
def extract_album_and_tracks_to_df(album_details, tracks):
    # Extract album information
    album_info = {
        'Album Name': album_details.get('name', 'Unknown Album'),
        'Album URI': album_details.get('uri', 'Unknown URI'),
        'Release Date': album_details.get('release_date', 'Unknown Release Date'),
        'Total Tracks': album_details.get('total_tracks', 'Unknown Total Tracks'),
        'Album Type': album_details.get('type', 'Unknown Type'),
        'Genres': ", ".join(album_details.get('genres', [])),  # Genres should come from album_details
        'Artists': ", ".join([artist['name'] for artist in album_details.get('artists', [])]),
    }
    
    # Create a list to store all the track data
    track_data = []
    
    # Loop through each track and combine with album info
    for track in tracks:
        track_data.append({
            'Track Name': track.get('name', 'Unknown Track'),
            'Track URI': track.get('uri', 'Unknown URI'),
            'Popularity': track.get('popularity', 'Unknown Popularity'),  # Get popularity from track
            'Duration (ms)': track.get('duration_ms', 'Unknown Duration'),
            'Track Number': track.get('track_number', 'Unknown Track Number'),
            'Album Name': album_info['Album Name'],
            'Album URI': album_info['Album URI'],
            'Release Date': album_info['Release Date'],
            'Artists': album_info['Artists'],
            'Genres': album_info['Genres'],  # Genres from album details
        })
    
    # Convert track data to DataFrame
    df = pd.DataFrame(track_data)
    return df


# Usage
client_id = "b4f43b6c79cf43f5a4be261bd44163b7"
client_secret = "a9775e34947341249bc7edbf9b2864c3"
playlist_id = "5T7dYFyHm6lhIuzj2XpDOZ"  # Specify your playlist ID here
album_id="3kjHLu1pL7tdY88GFwEkl6"

# Get access token and top tracks
spotify_token = get_spotify_token(client_id, client_secret)
#TEST
#top_tracks = get_spotify_top_tracks(spotify_token, playlist_id)
# Extract all track information to a DataFrame
#tracks_df = extract_all_tracks_to_df(top_tracks)
#print(tracks_df)



album_details = get_album_details(spotify_token, album_id)
tracks = get_spotify_album_tracks(spotify_token, album_id)
album_tracks_df = extract_album_and_tracks_to_df(album_details, tracks)
print(tracks)

