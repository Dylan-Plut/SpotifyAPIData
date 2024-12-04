import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

# Set up authentication credentials and scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="######",
                                               client_secret="######",
                                               redirect_uri="http://localhost:3000",
                                               scope="user-top-read"))


def get_top_artists(limit=100):
    # Retrieve top artists
    all_artists = []
    for offset in range(0, limit, 50):  # Spotify allows max 50 items per request
        results = sp.current_user_top_artists(limit=50, offset=offset,
                                              time_range='long_term')

        # Append the current batch of results
        for item in results['items']:
            artist_info = {
                'name': item['name'],
                'id': item['id'],
                'popularity': item['popularity'],
                'genres': item['genres'],
                'followers': item['followers']['total'],
            }
            all_artists.append(artist_info)

    return all_artists


def save_to_csv(artists, filename="top_artists.csv"):
    # Define the CSV header
    fieldnames = ['name', 'id', 'popularity', 'genres', 'followers']

    # Write data to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        writer.writerows(artists)  # Write the artist data

    print(f"Top artists data saved to {filename}")


def main():
    top_artists = get_top_artists(limit=100)
    save_to_csv(top_artists, filename="CSV_Files/top_artists.csv")


if __name__ == "__main__":
    main()
