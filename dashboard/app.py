import streamlit as st
from data_loader import load_data
from components import peliculas, camaras, generos

st.set_page_config(
    page_title='Cue', 
    layout='wide'
)

#CSS
from pathlib import Path

def load_css(relative_path):
    css_path = Path(__file__).parent / relative_path
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

df, df_cameras = load_data()

st.markdown('<h1 class = "main-title">Cue</h1>', unsafe_allow_html=True)
st.markdown('<p class = "sub-title">Film data analytics for the independent sector. Insights and trends from the film guild.</p>', unsafe_allow_html=True)

st.sidebar.markdown("### Filters")

decades = sorted(df['decade'].dropna().unique().astype(int).tolist())
selected_decades = st.sidebar.multiselect(
    'Decade',
    options=decades,
    default=decades
)

languages = sorted(df['original_language'].dropna().unique().tolist())
selected_languages = st.sidebar.multiselect(
    'Original Language',
    options=languages,
    default=['en']
)

df_filtered = df[
    df['decade'].isin(selected_decades) &
    df['original_language'].isin(selected_languages)
]

st.sidebar.markdown(f'<div class="filter-count"><b>{len(df_filtered)}</b> films selected</div>', unsafe_allow_html=True)

tab_movies, tab_cameras, tab_genres = st.tabs(['Movies', 'Cameras', 'Genres']) 

with tab_movies: peliculas.render(df_filtered)
with tab_cameras: camaras.render(df_cameras)
with tab_genres: generos.render(df_filtered)

