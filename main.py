from bs4 import BeautifulSoup
import requests 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os 
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
RETURN_URL = "http://example.com"

input_date = ""
    
def get_billboard_songs():
    URL = "https://www.billboard.com/charts/hot-100/"
    input_date = input("Enter the date in YYYY-MM-DD format: ")
    response = requests.get(url = f"{URL}{input_date}")
    soup = BeautifulSoup(response.text, "html.parser")
    song_title = soup.select("div ul li ul li h3")
    #change the song into clean text 
    songs = [song.getText().strip("\n\t") for song in song_title]
    #print(songs)
    return songs, input_date
def create_playlist(input_date,user_id):
    return sp.user_playlist_create(
        user= user_id,
        name=f"Top 100 songs of {input_date}",
        public=False,
        description=f"Album of top 100 songs from billboads of {input_date}"

    )
    

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id= CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri= RETURN_URL,
        scope= "playlist-modify-private",
        cache_path="token.txt",
        show_dialog=True,
    )
)
  
user_id = sp.current_user()["id"]
songs ,input_date = get_billboard_songs()
playlist = create_playlist(input_date = input_date, user_id=user_id)

song_uris =[]
year = input_date.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't simply exist in spotify")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

                        