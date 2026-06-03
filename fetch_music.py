import requests
import pandas as pd
from datetime import datetime

def fetch_tracks(genre, limit=50):
    url = "https://itunes.apple.com/search"
    params = {
        "term": genre,
        "mediaType": "music",
        "limit": limit,
        "entity": "song"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["results"]

def parse_tracks(tracks):
    records = []
    for track in tracks:
        records.append({
            "track": track.get("trackName"),
            "artist": track.get("artistName"),
            "album": track.get("collectionName"),
            "genre": track.get("primaryGenreName"),
            "price": track.get("trackPrice"),
            "release_date": track.get("releaseDate", "")[:10]
        })
    return pd.DataFrame(records)

def summarise(df):
    print(f"\n--- Music Data Summary ---")
    print(f"Total tracks fetched: {len(df)}")
    print(f"\nTop 5 Artists by track count:")
    print(df["artist"].value_counts().head())
    print(f"\nGenres found:")
    print(df["genre"].value_counts())

if __name__ == "__main__":
    genre = "rap"  # change this to anything you like
    print(f"Fetching tracks for: {genre}")
    raw = fetch_tracks(genre)
    df = parse_tracks(raw)
    filename = f"tracks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}")
    summarise(df)