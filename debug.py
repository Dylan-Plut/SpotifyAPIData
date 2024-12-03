import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
import os


def get_spotify_credentials():
    """
    Retrieve Spotify credentials from environment variables or prompt user.
    """
    client_id = os.environ.get('fb72b900efce4528865229d9d5211a16')
    client_secret = os.environ.get('44eb1cb44c2b44349f70f6dc3c623de7')

    if not client_id or not client_secret:
        print("Spotify API credentials not found in environment variables.")
        print("Please set the following environment variables:")
        print("SPOTIPY_CLIENT_ID")
        print("SPOTIPY_CLIENT_SECRET")
        print("\nOr enter them manually:")
        client_id = input("Enter Spotify Client ID: ").strip()
        client_secret = input("Enter Spotify Client Secret: ").strip()

    return client_id, client_secret


def extract_track_id_from_url(spotify_url):
    """
    Extract the Spotify track ID from a Spotify URL.
    """
    if not isinstance(spotify_url, str):
        return None

    match = re.search(r'/track/([a-zA-Z0-9]+)', spotify_url)
    return match.group(1) if match else None


def fetch_track_audio_features():
    """
    Fetch audio features (specifically danceability) for tracks from the CSV.

    Prerequisites:
    1. Install required libraries:
       pip install spotipy pandas
    2. Set up Spotify Developer credentials
    """
    # Get Spotify credentials
    client_id, client_secret = get_spotify_credentials()

    # Set up Spotify authentication (Client Credentials Flow)
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Verify authentication by getting a simple user profile
        sp.current_user_top_tracks(limit=1)
    except Exception as auth_error:
        print("Authentication failed. Please check your credentials:")
        print(f"Error: {auth_error}")
        return None

    try:
        # Read the tracks CSV
        tracks_df = pd.read_csv('artists_top_tracks.csv')

        # Prepare to store track audio features
        track_features_data = []

        # Extract track IDs and fetch audio features in batches
        track_ids = tracks_df['Top Track URL'].apply(extract_track_id_from_url).tolist()

        # Remove any None values
        track_ids = [tid for tid in track_ids if tid is not None]

        # Print track IDs for debugging
        print("Track IDs:", track_ids)

        # Spotify API allows fetching audio features for up to 100 tracks at once
        for i in range(0, len(track_ids), 50):
            batch_ids = track_ids[i:i + 50]

            # Detailed error handling for audio features
            try:
                audio_features_batch = sp.audio_features(batch_ids)
            except spotipy.exceptions.SpotifyException as api_error:
                print(f"Spotify API Error: {api_error}")
                print(f"Status Code: {api_error.http_status}")
                print(f"Error Details: {api_error}")
                continue

            # Process audio features for this batch
            for j, features in enumerate(audio_features_batch):
                if features:
                    # Combine original track info with audio features
                    track_info = tracks_df[tracks_df['Top Track URL'].apply(
                        lambda x: extract_track_id_from_url(x) == batch_ids[j])].iloc[0]

                    track_features = {
                        'Artist Name': track_info['Artist Name'],
                        'Top Track Name': track_info['Top Track Name'],
                        'Album': track_info['Album'],
                        'Danceability': features.get('danceability', None),
                        'Energy': features.get('energy', None),
                        'Key': features.get('key', None),
                        'Tempo': features.get('tempo', None)
                    }
                    track_features_data.append(track_features)

        # Create DataFrame of track features
        features_df = pd.DataFrame(track_features_data)

        # Save to CSV
        features_df.to_csv('track_audio_features.csv', index=False)

        print("Track audio features have been saved to 'track_audio_features.csv'")
        return features_df

    except FileNotFoundError:
        print("Error: 'artists_top_tracks.csv' file not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def main():
    # Fetch track audio features
    track_features = fetch_track_audio_features()

    if track_features is not None:
        print("\nTrack Audio Features:")
        print(track_features)

        # Display danceability levels
        print("\nDanceability Levels:")
        for _, row in track_features.iterrows():
            print(f"{row['Artist Name']} - {row['Top Track Name']}: {row['Danceability']:.2f}")


if __name__ == '__main__':
    main()

# Troubleshooting Notes:
# 1. Ensure Spotify Developer credentials are correct
# 2. Verify track IDs are valid
# 3. Check network connection
# 4. Ensure you have the latest version of spotipy
"""
Troubleshooting Setup:
1. Install/update dependencies:
   pip install --upgrade spotipy pandas
2. Set Spotify Developer credentials
3. Ensure correct CSV file
4. Check network connection
"""