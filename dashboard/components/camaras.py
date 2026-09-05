import streamlit as st
import plotly.express as px

def render(df_cameras):

    st.header('Cameras')

    col1, col2, col3 = st.columns(3)
    col1.metric('Total cameras', len(df_cameras))
    col2.metric('Brands', df_cameras['brand'].nunique())
    col3.metric('Categories', df_cameras['category'].nunique())

    st.subheader('Cameras by brand')
    st.caption(f'Distribution of {len(df_cameras)} cinema cameras across {df_cameras["brand"].nunique()} brands in Cue\'s collection.')
    
    brand_counts = df_cameras['brand'].value_counts().reset_index()
    brand_counts.columns = ['brand', 'count']
    
    fig = px.bar(
        brand_counts,
        x='brand',
        y='count',
        color_discrete_sequence=['#7B2D8B']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Brand',
        yaxis_title='Number of cameras'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Camera Specs')
    st.caption('Find info to compare technical specifications across cameras. Select a brand to filter!')
    
    brands = ['All'] + sorted(df_cameras['brand'].unique().tolist())
    selected_brand = st.selectbox('Brand', options=brands)
    
    # Cam filter  
    df_cam_filtered = df_cameras if selected_brand == 'All' else df_cameras[df_cameras['brand'] == selected_brand]
    
    st.dataframe(
        df_cam_filtered[['brand', 'model', 'category', 'sensor_size', 'resolution_k', 'dynamic_range', 'iso_native', 'price_usd_approx']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown('<p style="font-size: 18px; font-weight: 600; color: #E8E8E8;">Can\'t find a camera?</p>', unsafe_allow_html=True)
    st.caption("Leave a suggestion so we can add it to the database.")

    with st.form('camera_suggestion'):
        camera_name = st.text_input('Camera name')
        brand_name = st.text_input('Brand')
        notes = st.text_area('Any additional notes? (optional)')
        submitted = st.form_submit_button('Send suggestion')

    if submitted:
        if camera_name and brand_name:
            import requests
            response = requests.post(
                'https://formspree.io/f/meaqznbj',
                data={
                    'camera': camera_name,
                    'brand': brand_name,
                    'notes': notes
                }
            )
            if response.status_code == 200:
                st.success('Thank you, your suggestion was sent.')
            else:
                st.error('Something went wrong. Please try again.')
        else:
            st.warning('Please fill in the camera name and brand.')
            