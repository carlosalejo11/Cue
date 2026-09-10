import ast
import plotly.express as px
import streamlit as st


def render(df_filtered):
    st.header('Genres')
    st.subheader('Risk vs Return (by genre)')
    st.caption('Median ROI vs Risk Ratio for genres with at least 5 films.')

    if df_filtered.empty:
        st.warning('No films match the selected filters.')
        return

    df_exploded = df_filtered.copy()
    if 'genres' in df_exploded.columns:
        df_exploded['genres'] = df_exploded['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
        df_exploded = df_exploded.explode('genres')

    genres_performance = (
        df_exploded.groupby('genres', as_index=False)['roi']
        .agg(['median', 'std', 'count'])
        .round(2)
    )

    genres_performance.columns = ['genre', 'median_roi', 'roi_std', 'movie_count']
    genres_performance = genres_performance[
    genres_performance['movie_count'] >= 5
    ]

    if genres_performance.empty:
        st.info(
        'There isn\'t enough data in current selection to calculate Risk vs Return'
        ' (minimum 5 films per genre are required).'
    )
        return

    genres_performance['risk_ratio'] = (genres_performance['roi_std'] / genres_performance['median_roi'])

    fig = px.scatter(
        genres_performance,
        x='risk_ratio',
        y='median_roi',
        size='movie_count',
        text='genre',
        color_discrete_sequence=['#9D4EDD'],
        log_x=True,
        log_y=True,
    )

    fig.update_traces(textposition='top center')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Risk ratio (log scale)',
        yaxis_title='Median ROI % (log scale)',
    )
    
    st.plotly_chart(fig, use_container_width=True)