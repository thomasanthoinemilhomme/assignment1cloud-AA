import os
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import json



def autocomplete_titles(client, partial_title):
    QUERY = f"""
    SELECT title
    FROM `crafty-acumen-406617.movie_1.movies`
    WHERE LOWER(title) LIKE LOWER('%{partial_title}%')
    LIMIT 10
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [row.title for row in results]

def filter_by_genre(client, genre):
    QUERY = f"""
    SELECT *
    FROM `crafty-acumen-406617.movie_1.movies`
    WHERE genres LIKE '%{genre}%'
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [row for row in results]

def filter_by_rating(client):
    QUERY = """
    SELECT m.movieId, m.title, AVG(r.rating) as avg_rating
    FROM crafty-acumen-406617.movie_1.movies m
    JOIN crafty-acumen-406617.movie_1.movie_ratings r ON m.movieId = r.movieId
    GROUP BY m.movieId, m.title
    HAVING AVG(r.rating) > 4.0
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [(row.movieId, row.title, row.avg_rating) for row in results]
    
def filter_by_rating(client):
    QUERY = """
    SELECT m.movieId, m.title, AVG(r.rating) as avg_rating
    FROM crafty-acumen-406617.movie_1.movies m
    JOIN crafty-acumen-406617.movie_1.movie_ratings r ON m.movieId = r.movieId
    GROUP BY m.movieId, m.title
    HAVING AVG(r.rating) > 4.0
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [(row.movieId, row.title, row.avg_rating) for row in results]

def filter_by_release_year(client, year=2019):
    QUERY = f"""
    SELECT *
    FROM crafty-acumen-406617.movie_1.movies
    WHERE release_year > {year}
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [row for row in results]

st.title('BigQuery Movie Explorer')

# Autocomplete example
title_input = st.text_input('Search movie titles')
if title_input:
    titles = autocomplete_titles(client, title_input)
    st.write('Results:', titles)

# Genre filter example
genre = st.selectbox('Select a genre', ['Comedy', 'Drama', 'Romance', 'Action', 'Thriller'])
if st.button('Filter by Genre'):
    movies = filter_by_genre(client, genre)
    for movie in movies:
        st.write(movie)

# Rating filter example
if st.button('Show Highly Rated Movies'):
    highly_rated_movies = filter_by_rating(client)
    for movie in highly_rated_movies:
        st.write(movie)

# Release year filter example
year = st.slider('Select release year', min_value=1980, max_value=2021, value=2019)
if st.button('Filter by Release Year'):
    recent_movies = filter_by_release_year(client, year)
    for movie in recent_movies:
        st.write(movie)
    

client = bigquery.Client()

