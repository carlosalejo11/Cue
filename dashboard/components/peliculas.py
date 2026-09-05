import streamlit as st
import plotly.express as px

def render(df_filtered, df_genres, df_genre_roi, df_decade):

# First graphic

    st.header('Films')

    col1, col2, col3 = st.columns(3)
    col1.metric('Total films', len(df_filtered))
    col2.metric('Avg budget', f"${df_filtered['budget'].median()/1_000_000:.1f}M")
    col3.metric('Avg ROI', f"{df_filtered['roi'].median():.1f}%")

    st.subheader('Most frequent genres')
    st.caption(f'Here is the distribution of genres across {len(df_filtered)} films in the selected filters.')
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
        xaxis_title='Films',
        yaxis_title=''
    )
    st.plotly_chart(fig, use_container_width=True)
    
# Second graphic

    st.subheader('Median ROI by genre')
    st.caption(f'Return of Investment = (Revenue - Budget) based on {len(df_filtered)} films, uses median ROI to avoid outliers.')
    fig2 = px.bar(
        df_genre_roi.sort_values('avg_roi', ascending=True),
        x='avg_roi',
        y='genre',
        orientation='h',
        color_discrete_sequence=['#7B2D8B']
    )
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Median ROI (%)',
        yaxis_title=''
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader('Films per decade')
    st.caption(f'The number of films released per decade, based on the selected filters.')
    fig3 = px.line(
        df_decade,
        x='decade',
        y='movie_count',
        markers=True,
        color_discrete_sequence=['#7B2D8B']
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Decade',
        yaxis_title='Films'
    )
    st.plotly_chart(fig3, use_container_width=True)