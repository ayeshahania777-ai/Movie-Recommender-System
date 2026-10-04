import pickle
import requests
import streamlit as st


# ============================================================
# 1. LOAD MOVIE DATA AND SIMILARITY MODEL
# ============================================================

movies = pickle.load(
    open("model/movie_list.pkl", "rb")
)

similarity = pickle.load(
    open("model/similarity.pkl", "rb")
)


# ============================================================
# 2. FETCH MOVIE POSTER
# ============================================================

def fetch_poster(movie_id):

    # Add your NEW TMDB API key here later
    api_key = "YOUR_NEW_TMDB_API_KEY"

    if api_key == "YOUR_NEW_TMDB_API_KEY":
        return None

    url = (
        "https://api.themoviedb.org/3/movie/"
        + str(movie_id)
        + "?api_key="
        + api_key
        + "&language=en-US"
    )

    try:

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return (
                "https://image.tmdb.org/t/p/w500/"
                + poster_path
            )

        return None

    except Exception:
        return None


# ============================================================
# 3. RECOMMEND MOVIES
# ============================================================

def recommend(movie):

    # Find selected movie
    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Sort movies according to similarity
    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for index, score in movie_indices:

        movie_id = movies.iloc[index]["movie_id"]

        movie_name = movies.iloc[index]["title"]

        poster = fetch_poster(movie_id)

        recommended_movie_names.append(movie_name)

        recommended_movie_posters.append(poster)

    return (
        recommended_movie_names,
        recommended_movie_posters
    )


# ============================================================
# 4. STREAMLIT PAGE
# ============================================================

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# 5. TITLE
# ============================================================

st.title("🎬 Movie Recommender System")

st.write(
    "Select a movie and discover similar movies."
)


# ============================================================
# 6. MOVIE DROPDOWN
# ============================================================

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)


# ============================================================
# 7. RECOMMEND BUTTON
# ============================================================

if st.button("🎯 Show Recommendation"):

    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie
    )

    st.subheader(
        "Recommended Movies"
    )

    # Create 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [
        col1,
        col2,
        col3,
        col4,
        col5
    ]

    # Display recommendations
    for i in range(5):

        with columns[i]:

            st.markdown(
                f"### {recommended_movie_names[i]}"
            )

            if recommended_movie_posters[i]:

                st.image(
                    recommended_movie_posters[i],
                    use_container_width=True
                )

            else:

                st.info(
                    "Poster not available"
                )