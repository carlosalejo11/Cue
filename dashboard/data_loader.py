import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / 'data' / 'processed'

# Dashboard data load 
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH / 'tmdb_clean.csv')
    # A decade column was needed for the decade filter in the dashboard
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['release_year'] = df['release_date'].dt.year
    df['decade'] = (df['release_year'] // 10) * 10
    df_cameras = pd.read_csv(DATA_PATH / 'cinema_cameras_clean.csv')
    df_genres = pd.read_csv(DATA_PATH / 'genre_counts.csv')
    df_genre_roi = pd.read_csv(DATA_PATH / 'genre_roi.csv')
    df_decade = pd.read_csv(DATA_PATH / 'movies_per_decade.csv')
    return df, df_cameras, df_genres, df_genre_roi, df_decade