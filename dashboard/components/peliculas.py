import ast
import pandas as pd
import plotly.express as px
import streamlit as st


def render(df_filtered):
    st.header('Films')

    if df_filtered.empty:
        st.warning('⚠️ No films match the selected filters.')
        return

    col1, col2, col3 = st.columns(3)
    col1.metric('Total films', len(df_filtered))

    budget_median = (
        df_filtered['budget'].median() if 'budget' in df_filtered.columns else 0
    )
    roi_median = df_filtered['roi'].median() if 'roi' in df_filtered.columns else 0

    col2.metric('Avg budget', f'${budget_median/1_000_000:.1f}M')
    col3.metric('Avg ROI', f'{roi_median:.1f}%')

    df_exp = df_filtered.copy()
    if 'genres' in df_exp.columns:
        df_exp['genres_clean'] = df_exp['genres'].apply(
            lambda x: (
                ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x
            )
        )
        df_exploded = df_exp.explode('genres_clean')
        genre_col = 'genres_clean'
    else:
        df_exploded = df_exp
        genre_col = 'genre' if 'genre' in df_exp.columns else None

    st.subheader('Most frequent genres')
    st.caption(
        f'Distribution of genres across {len(df_filtered)} selected films.'
    )

    if genre_col and genre_col in df_exploded.columns:
        df_genres = (
        df_exploded.groupby(genre_col)
        .size()
        .reset_index(name='count')
        .rename(columns={genre_col: 'genre'})
    )

    fig1 = px.bar(
        df_genres.sort_values('count', ascending=True),
        x='count',
        y='genre',
        orientation='h',
        color_discrete_sequence=['#9D4EDD'],
    )
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Films',
        yaxis_title='',
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader('Median ROI by genre')
    st.caption(
        'Return on Investment = (Revenue - Budget) using median to avoid'
        ' outliers.'
    )

    if (
        genre_col
        and genre_col in df_exploded.columns
        and 'roi' in df_exploded.columns
    ):
        df_genre_roi = (
        df_exploded.groupby(genre_col)['roi']
        .median()
        .reset_index(name='avg_roi')
        .rename(columns={genre_col: 'genre'})
    )

    fig2 = px.bar(
        df_genre_roi.sort_values('avg_roi', ascending=True),
        x='avg_roi',
        y='genre',
        orientation='h',
        color_discrete_sequence=['#7B2CBF'],
    )
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Median ROI (%)',
        yaxis_title='',
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader('Films per decade')
    st.caption('Number of films released per decade based on selected filters.')

    if 'decade' in df_filtered.columns:
        df_decade = (
        df_filtered.groupby('decade')
        .size()
        .reset_index(name='movie_count')
        .sort_values('decade')
    )

    fig3 = px.line(
        df_decade,
        x='decade',
        y='movie_count',
        markers=True,
        color_discrete_sequence=['#E0AAFF'],
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Decade',
        yaxis_title='Films',
    )
    st.plotly_chart(fig3, use_container_width=True)