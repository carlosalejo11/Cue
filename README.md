# Cue - Film Analytics
Cue is an interactive platform where you'll find statistics, trends and comparisons about the movie industry. 

APP: [cuecinema.streamlit.app](https://cuecinema.streamlit.app)

## Technologies: 
    Data processing using Pandas and NumPy
    Frontend / Dashboard with Python 3.11 using Streamlit
    Visualization with Plotly
    Launched in Streamlit Community Cloud

## Project Structure: 
    Cue/
        dashboard/
            app.py              - Streamlit application 
            data_loader.py      - Data loading module
            assets/             - CSS styling
            components/         - Modules
        data/                   - Datasets 
        requirements.txt        - Dependencies 
        README.md               - Documentation

## API
Cue includes a REST API built with Node.js and Express. Here the datasets are exposed as JSON endpoints. 
If you want to run it locally: 

    cd api
    npm install
    noder server.js

Endpoints:
    GET /peliculas              - List of films
    GET /peliculas/:id          - Film by TMDB ID
    GET /camaras                - Cameras database
    GET /generos                - Genre data    