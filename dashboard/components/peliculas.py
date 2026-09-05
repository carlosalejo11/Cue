import streamlit as st
import plotly.express as px

def render(df_filtered, df_genres, df_genre_roi, df_decade):

    st.header('Films')

    col1, col2, col3 = st.columns(3)
    col1.metric('Total films', len(df_filtered))
    col2.metric('Avg budget', f"${df_filtered['budget'].median()/1_000_000:.1f}M")
    col3.metric('Avg ROI', f"{df_filtered['roi'].median():.1f}%")

    st.subheader('Most frequent genres')
    fig = px.bar(
        df_genres.sort_values('count', ascending=True),
        x='count',
        y='genre',
        orientation='h',
        color_discrete_sequence=['#7B2D8B']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Number of films',
        yaxis_title=''
    )
    st.plotly_chart(fig, use_container_width=True)
    
