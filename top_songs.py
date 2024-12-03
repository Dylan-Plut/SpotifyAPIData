import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json

"""
Set ENV Variables
SPOTIPY_CLIENT_ID='your_client_id'
SPOTIPY_CLIENT_SECRET='your_client_secret'
"""


def fetch_top_songs_for_artists():
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    try:
        artists_df = pd.read_csv('top_artists.csv')
        top_songs_data = []
        for _, artist in artists_df.iterrows():
            artist_name = artist['name']
            artist_id = artist['id']
            try:
                top_tracks = sp.artist_top_tracks(artist_id)
                if top_tracks['tracks']:
                    top_track = top_tracks['tracks'][0]
                    top_song_info = {
                        'Artist Name': artist_name,
                        'Top Track Name': top_track['name'],
                        'Top Track Popularity': top_track['popularity'],
                        'Top Track URL': top_track['external_urls']['spotify'],
                        'Album': top_track['album']['name']
                    }
                    top_songs_data.append(top_song_info)
                else:
                    print(f"No top tracks found for {artist_name}")
            except Exception as artist_error:
                print(f"Error fetching top track for {artist_name}: {artist_error}")
        top_songs_df = pd.DataFrame(top_songs_data)
        top_songs_df.to_csv('artists_top_tracks.csv', index=False)
        print("Top tracks for artists have been saved to 'artists_top_tracks.csv'")
        return top_songs_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    top_songs = fetch_top_songs_for_artists()
    if top_songs is not None:
        print("\nTop Tracks for Artists:")
        print(top_songs)


if __name__ == '__main__':
    main()
