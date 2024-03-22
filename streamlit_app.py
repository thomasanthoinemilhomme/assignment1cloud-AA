import os
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import json
import requests
import pandas as pd
import re

client = bigquery.Client()

def autocomplete_titles(client, partial_title):
    QUERY = f"""
    SELECT title
    FROM `crafty-acumen-406617.movies_1.movies`
    WHERE LOWER(title) LIKE LOWER('%{partial_title}%')
    LIMIT 10
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [row.title for row in results]

def filter_by_genre(client, genre):
    QUERY = f"""
    SELECT *
    FROM `crafty-acumen-406617.movies_1.movies`
    WHERE genres LIKE '%{genre}%'
    LIMIT 30
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [row for row in results]

def filter_by_rating(client, min_rating):
    QUERY = f"""
    SELECT m.movieId, m.title, AVG(r.rating) as avg_rating
    FROM `crafty-acumen-406617.movies_1.movies` m
    JOIN `crafty-acumen-406617.movies_1.movie_ratings` r ON m.movieId = r.movieId
    GROUP BY m.movieId, m.title
    HAVING AVG(r.rating) > {min_rating}
    LIMIT 30
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [(row.movieId, row.title, row.avg_rating) for row in results]


    

def filter_by_release_year(client, year=2019):
    QUERY = f"""
    SELECT *
    FROM crafty-acumen-406617.movies_1.movies
    WHERE release_year > {year}
    """
    query_job = client.query(QUERY)
    results = query_job.result()
    return [row for row in results]


def preprocess_title(title_with_date):
    # Regex to find and remove the date in parentheses at the end of the title
    title_without_date = re.sub(r'\s*\(\d{4}\)$', '', title_with_date)
    return title_without_date

def fetch_movie_details_and_cover(title, api_key):
    url = "http://www.omdbapi.com/"
    params = {"t": title, "apikey": api_key}
    response = requests.get(url, params=params)
    print("Requesting URL:", response.url)  # Print the URL being requested
    if response.status_code == 200:
        movie_data = response.json()
        print("Response Data:", movie_data)  # Print the response data
        if movie_data["Response"] == "True":
            return {
                "title": movie_data.get("Title"),
                "year": movie_data.get("Year"),
                "genre": movie_data.get("Genre"),
                "director": movie_data.get("Director"),
                "actors": movie_data.get("Actors"),
                "plot": movie_data.get("Plot"),
                "poster_url": movie_data.get("Poster", None)
            }
        else:
            print("Error from OMDB API:", movie_data.get("Error", "Unknown Error"))  # Print any errors returned by the API
            return {"error": "Movie not found or API limit exceeded."}
    else:
        return {"error": "Failed to fetch data from OMDB API."}


def fetch_movie_cover(title, api_key):
    """Fetch movie cover image URL by title."""
    url = "http://www.omdbapi.com/"
    params = {"t": title, "apikey": api_key}
    response = requests.get(url, params=params)
    movie_data = response.json()

    # Return the poster URL or None if not found
    return movie_data.get("Poster")

def display_movie_info(raw_title, api_key):

    title = preprocess_title(raw_title)
    movie_data = fetch_movie_details_and_cover(title, api_key)
    api_call_successful = movie_data.get('error') is None
    # Check if there's an error key in the returned dictionary
    if movie_data:
        # Layout for movie details
        col1, col2 = st.columns(2)

        with col1:  # Display movie details fetched from BigQuery
            st.header(movie_details["title"])
            st.subheader(f"Year: {movie_details['year']}")
            st.write(f"**Genre:** {movie_details['genre']}")
            st.write(f"**Director:** {movie_details.get('director', 'N/A')}")
            st.write(f"**Cast:** {movie_details.get('actors', 'N/A')}")
            st.write(f"**Plot:** {movie_details.get('plot', 'N/A')}")

        with col2:  # Attempt to fetch and display the movie poster
            poster_url = fetch_movie_cover(title, api_key) if api_key else "https://via.placeholder.com/200x300?text=Poster+Not+Available"
            if poster_url and poster_url != "N/A":
                st.image(poster_url, caption="Movie Poster", width=300)
            else:
                st.write("Poster not available.")
    else:
        # Display an error message if movie details couldn't be fetched from BigQuery
        st.error("Movie details not found in the database.") 



OMDB_API_KEY = "6ba470"



st.title('BitQuery Movie Explorer')

# Autocomplete example
title_input = st.text_input('Search movie titles')
if title_input:
    titles = autocomplete_titles(client, title_input)
    display_movie_info(title_input, OMDB_API_KEY)

genre = st.selectbox('Select a genre', ['Action', 'Comedy', 'Drama', 'Romance', 'Sci-Fi'])

if st.button('Filter by Genre'):
    movies = filter_by_genre(client, genre)
    for movie in movies:
        processed_title = preprocess_title(movie.title)  # Preprocess the title to remove dates, etc.
        display_movie_info(processed_title, OMDB_API_KEY)  # Use the processed title for API calls
# Rating filter example
min_rating = st.slider('Minimum average rating', 0.0, 5.0, 4.0)

if st.button('Filter by Rating'):
    movies = filter_by_rating(client, min_rating)
    for movie in movies:
        display_movie_info(movie[1], OMDB_API_KEY)

min_year = st.slider('Select minimum release year', 1900, 2021, 2010)

if st.button('Filter by Release Year'):
    movies = filter_by_release_year(client, min_year)
    for movie in movies:
        display_movie_info(movie.title, OMDB_API_KEY)



