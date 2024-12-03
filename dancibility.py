import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

# Set up authentication credentials and scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ff4c30e99e6c48bb9deaf12fc44ad9ea",
                                               client_secret="0817ba394b8d48faaf1fb7fb710d8e37",
                                               redirect_uri="http://localhost:3000",
                                               scope="user-top-read user-library-read"))

def get_top_artists(limit=100):
    all_artists = []
    for offset in range(0, limit, 50):
        results = sp.current_user_top_artists(limit=50, offset=offset, time_range='long_term')
        for item in results['items']:
            all_artists.append(item['id'])  # Collecting only artist IDs
    return all_artists

def get_artist_top_tracks(artist_id):
    results = sp.artist_top_tracks(artist_id)
    return [track['id'] for track in results['tracks']]

def get_tracks_danceability(track_ids):
    danceabilities = []
    for i in range(0, len(track_ids), 50):  # Max 50 IDs per request
        audio_features = sp.audio_features(track_ids[i:i + 50])
        for features in audio_features:
            if features:
                danceabilities.append({
                    'track_id': features['id'],
                    'track_name': features['track_href'].split('/')[-1],  # Get track name from URL
                    'danceability': features['danceability']
                })
    return danceabilities

def save_danceability_to_csv(danceabilities, filename="danceability.csv"):
    fieldnames = ['track_id', 'track_name', 'danceability']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(danceabilities)
    print(f"Danceability data saved to {filename}")

def main():
    top_artists = get_top_artists(limit=100)
    all_track_ids = []
    for artist_id in top_artists:
        all_track_ids.extend(get_artist_top_tracks(artist_id))

    danceabilities = get_tracks_danceability(all_track_ids)
    save_danceability_to_csv(danceabilities, filename="danceability.csv")

if __name__ == "__main__":
    main()
