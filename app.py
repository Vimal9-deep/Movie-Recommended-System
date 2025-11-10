import streamlit as st
import pandas as pd 
import pickle # For loading pre-trained models or data

#function for fetching movie poster from API
import requests

def fetch_poster(movie_id):
  response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4bea04673df8fc321c83b8c9dfa1911f'.format(movie_id))
  data=response.json() 
  return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']

def recommend(movie):
  movie_index=movies[movies['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  
  recommended_movies=[]
  recommended_movies_posters=[]
  for i in movies_list:
    movie_id=movies.iloc[i[0]].movie_id
    recommended_movies.append(movies.iloc[i[0]].title)
    #fetch poster from API
    recommended_movies_posters.append(fetch_poster(movie_id))
  return recommended_movies, recommended_movies_posters
  
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

#loading similarity matrix from google drive 
#similarity.pkl file is too much large that could not be uploaded at github so , i had uploaded it to google drive and doing dynamic fetching here 
import gdown
import os  
import joblib
# File info
drive_file_id = "1fLopcrEot4pgJHrPBJBYNFNUD3JI0fKR"  #  file ID
file_name = "similarity.pkl"

# Download once and cache locally
if not os.path.exists(file_name):
    with st.spinner("Downloading large data file... (only first time)"):
        url = f"https://drive.google.com/uc?id={drive_file_id}"
        gdown.download(url, file_name, quiet=False)

# Now load your data
similarity = joblib.load(open(file_name, 'rb'))


st.markdown("<h1 style='text-align: center; color: white;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

selected_movie_name=st.selectbox(
  '🔍Pick a movie to get similar recommendations',
  movies['title'].values)

if st.button('Recommend'):
  names,posters=recommend(selected_movie_name)
  #code for displaying layout
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.text(names[0])
    st.image(posters[0])
    
  with col2:
    st.text(names[1])
    st.image(posters[1])
  
  with col3:
    st.text(names[2])
    st.image(posters[2])
    
  with col4:
    st.text(names[3])
    st.image(posters[3])
    
  with col5:
    st.text(names[4])
    st.image(posters[4])


  
