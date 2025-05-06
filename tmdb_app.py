import streamlit as st
import requests

# --- API Token ---
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmMDI3M2Q0OWU2NjI4YjY2OGJhZDRhOTQ3YjE3ZmVjMSIsIm5iZiI6MTc0NjUzNzMzOC40MTgsInN1YiI6IjY4MWEwYjdhZGM1YTNjM2NjNDg0ZGE2OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.F9ggpf-ZQtmKfsdNIUhJ6eYKdzxXJr2XUF9n8f8h5D0"  # Replace with your actual API token

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "accept": "application/json"
}

# --- Fetching data from TMDb ---
def fetch_data(endpoint, num_pages=5):
    all_results = []
    for page in range(1, num_pages + 1):
        base_url = f"https://api.themoviedb.org/3/{endpoint}&page={page}"
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            all_results.extend(response.json().get('results', []))
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
    return all_results

# --- Displaying movie or TV show cards ---
def display_movies(movies):
    for movie in movies:
        st.subheader(movie.get("title") or movie.get("name"))
        col1, col2 = st.columns([1, 3])
        with col1:
            poster = movie.get("poster_path")
            if poster:
                st.image(f"https://image.tmdb.org/t/p/w500{poster}", width=120)
        with col2:
            st.write(f"📅 Release Date: {movie.get('release_date') or movie.get('first_air_date')}")
            st.write(f"⭐ Rating: {movie.get('vote_average')} ({movie.get('vote_count')} votes)")
            st.write(movie.get("overview", "No overview available."))

# --- Displaying popular people ---
def display_people(people):
    for person in people[:10]:
        st.subheader(person["name"])
        profile = person.get("profile_path")
        if profile:
            st.image(f"https://image.tmdb.org/t/p/w500{profile}", width=150)
        st.write("Known for: " + ", ".join([p.get("title") or p.get("name", "") for p in person.get("known_for", [])]))

# --- Theme CSS ---
def apply_theme(dark_mode):
    if dark_mode:
        st.markdown("""
            <style>
                body {
                    background-color: #0e1117;
                    color: #f0f0f0;
                }
                .stApp {
                    background-color: #0e1117;
                    color: #f0f0f0;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                .stApp {
                    background-color: white;
                    color: black;
                }
            </style>
        """, unsafe_allow_html=True)

# --- Main App ---
def main():
    st.set_page_config(page_title="🎬 TMDb Explorer", layout="wide")

    # --- Sidebar: Theme toggle and menu ---
    dark_mode = st.sidebar.toggle("🌙 Dark Mode")
    apply_theme(dark_mode)

    st.title("🎬 Movie & TV Explorer")

    menu = ["Top Rated Movies", "Popular TV Shows", "Upcoming Movies", "Popular People"]
    choice = st.sidebar.selectbox("Select Category", menu)

    if choice == "Top Rated Movies":
        st.header("Top Rated Movies")
        movies = fetch_data("movie/top_rated?language=en-US", num_pages=20)  # Adjust num_pages as needed
        display_movies(movies)

    elif choice == "Popular TV Shows":
        st.header("Popular TV Shows")
        movies = fetch_data("tv/popular?language=en-US", num_pages=20)  # Adjust num_pages as needed
        display_movies(movies)

    elif choice == "Upcoming Movies":
        st.header("Upcoming Movies")
        movies = fetch_data("movie/upcoming?language=en-US", num_pages=20)  # Adjust num_pages as needed
        display_movies(movies)

    elif choice == "Popular People":
        st.header("Popular People")
        people = fetch_data("person/popular?language=en-US", num_pages=20)  # Adjust num_pages as needed
        display_people(people)

if __name__ == "__main__":
    main()
