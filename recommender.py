import pandas as pd
import random
import os

# Load datasets with encoding fix and error handling
try:
    games_df = pd.read_csv("datasets/games.csv", encoding="ISO-8859-1")
except FileNotFoundError:
    print("Error: games.csv file not found.")
    games_df = pd.DataFrame()

try:
    songs_df = pd.read_csv("datasets/songs.csv", encoding="ISO-8859-1")
except FileNotFoundError:
    print("Error: songs.csv file not found.")
    songs_df = pd.DataFrame()

try:
    quotes_df = pd.read_csv("datasets/quotes.csv", encoding="ISO-8859-1")
except FileNotFoundError:
    print("Error: quotes.csv file not found.")
    quotes_df = pd.DataFrame()

# Standardize column names
games_df.columns = games_df.columns.str.replace('ï»¿', '', regex=True).str.strip()
songs_df.columns = songs_df.columns.str.replace('ï»¿', '', regex=True).str.strip()
quotes_df.columns = quotes_df.columns.str.replace('ï»¿', '', regex=True).str.strip()

# Rename columns to match function expectations
games_df.rename(columns={"Game link": "Online Play Link"}, inplace=True)
songs_df.rename(columns={"Category": "Emotion"}, inplace=True)

# Drop unnecessary columns
games_df = games_df.loc[:, ~games_df.columns.str.contains('Unnamed')]

def get_recommendations(emotion):
    recommendations = {"games": [], "songs": [], "quotes": []}

    try:
        emotion = emotion.lower().strip()  # Standardizing text comparison

        # Get unique Games (4 max)
        if {"Emotion", "Game Name", "Online Play Link"}.issubset(games_df.columns):
            game_list = games_df[games_df["Emotion"].astype(str).str.lower().str.strip() == emotion][["Game Name", "Online Play Link"]].drop_duplicates()
            recommendations["games"] = random.sample(game_list.to_dict(orient="records"), min(len(game_list), 4)) if not game_list.empty else []

        # Get unique Songs (4 max)
        if {"Emotion", "Song Name", "Song Link"}.issubset(songs_df.columns):
            song_list = songs_df[songs_df["Emotion"].astype(str).str.lower().str.strip() == emotion][["Song Name", "Song Link"]].drop_duplicates()
            recommendations["songs"] = random.sample(song_list.to_dict(orient="records"), min(len(song_list), 4)) if not song_list.empty else []

        # Get unique Quotes (2 max)
        if {"Emotion", "Quote"}.issubset(quotes_df.columns):
            quote_list = quotes_df[quotes_df["Emotion"].astype(str).str.lower().str.strip() == emotion]["Quote"].drop_duplicates().tolist()
            recommendations["quotes"] = random.sample(quote_list, min(len(quote_list), 2)) if quote_list else []

    except Exception as e:
        print(f"Error in recommendations: {e}")

    return recommendations
