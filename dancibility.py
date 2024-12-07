import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv


###PLEASE SEE THE README FILE FOR AN EXPLANATION OF THIS CODE. #####
# Spotify API credentials (replace with your own)
CLIENT_ID = '######'
CLIENT_SECRET = '#######'

# Authenticate with API
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    print("Authenticated successfully with Spotify API.")
except Exception as e:
    print(f"Authentication failed: {e}")
    exit()

def fetch_danceability_for_top_artists(output_file='danceability_scores.csv'):
    """
    Fetches danceability scores for tracks of the top 50 artists and outputs the data to a CSV file.
    """
    try:
        # Top 50 artists
        top_artists = sp.search(q='genre:pop', type='artist', limit=50)
        artists = top_artists['artists']['items']

        if not artists:
            print("No artists found. Please verify the query.")
            return

        # Collect artist IDs
        artist_ids = [artist['id'] for artist in artists]

        # Danceability
        data = []
        for artist_id in artist_ids:
            top_tracks = sp.artist_top_tracks(artist_id)
            for track in top_tracks['tracks']:
                track_name = track['name']
                track_id = track['id']

                try:
                    # Get audio features
                    audio_features = sp.audio_features([track_id])
                    if audio_features and audio_features[0]:
                        danceability = audio_features[0]['danceability']
                        data.append([track_name, artist_id, track_id, danceability])
                except spotipy.exceptions.SpotifyException as e:
                    print(f"Error fetching audio features for track {track_name} ({track_id}): {e}")
                except Exception as e:
                    print(f"Unexpected error fetching audio features for track {track_name} ({track_id}): {e}")

        # Write to CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Track Name', 'Artist ID', 'Track ID', 'Danceability'])
            writer.writerows(data)

        print(f"Danceability scores saved to {output_file}")

    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    fetch_danceability_for_top_artists()
