import streamlit as st
from data_loader import load_data

st.set_page_config(
    page_title='Cue',
    page_icon = '🎬',   
    layout='wide'
)

df, df_cameras, df_genres, df_genre_roi, df_decade = load_data()

st.title('Cue')
st.markdown('Film data analytics for the independent sector. Insights and trends from the film guild.')

st.sidebar.title('Filters')

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

st.sidebar.markdown(f'**{len(df_filtered)} films selected**')

from components import peliculas 
peliculas.render(df_filtered, df_genres, df_genre_roi, df_decade)