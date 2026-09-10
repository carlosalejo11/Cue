import streamlit as st
import plotly.express as px 

def render(df_filtered, df_genre_roi):
    st.header('Genres')
    st.subheader ('Risk V Return by genre')
    st.caption('Median Roi vs Risk Ratio (low budget films)') 
    
    import ast 
    df_exploded = df_filtered.copy()
    df_exploded['genres'] = df_exploded['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    genres_performance = (df_exploded.explode('genres').groupby('genres', as_index=False)['roi'].agg(['median', 'std', 'count']).round(2))
    # Genres dataframe 
    genres_performance.columns = ['genre', 'median_roi', 'roi_std', 'movie_count']
    genres_performance = genres_performance[genres_performance['movie_count'] >= 5]
    genres_performance['risk_ratio'] = genres_performance['roi_std'] / genres_performance['median_roi']
    
    fig = px.scatter(genres_performance, 
                    x='risk_ratio', 
                    y='median_roi', 
                    size='movie_count', 
                    text='genre', 
                    color_discrete_sequence=['#7B2D8B'],
                    log_x=True, log_y=True)
    
    fig.update_traces(textposition='top center')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title='Risk ratio (log scale)', yaxis_title='Median ROI % (log scale)')
    st.plotly_chart(fig, use_container_width=True)
    fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title='Risk ratio (log scale)',
    yaxis_title='Median ROI % (log scale)',
    xaxis=dict(range=[0, 3]), #Limit x axis up to 1000 to avoid outliers
    yaxis=dict(range=[1, 4]) #Limit y axis up to 10000 to avoid outliers
)