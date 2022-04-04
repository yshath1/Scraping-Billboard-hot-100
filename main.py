from bs4 import BeautifulSoup
import lxml
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/" + date
response = requests.get(URL)
billboard = response.text
soup = BeautifulSoup(billboard, "lxml")
song_titles = soup.find_all(name="h3", class_="c-title")
songs = []
year = date.split("-")[0]
for song in song_titles:
    songs.append(song.getText())
print(songs[0])
Client_ID = "707e54160c2647cf99ae0e4347dac568"
Client_Secret = "5e8f49249462428bb8d9b469ec2c5e7d"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=f"{Client_ID}",
                                               scope="playlist-modify-private",
                                               client_secret=f"{Client_Secret}",
                                               redirect_uri="http://example.com",
                                               show_dialog=True,
                                               cache_path="token.txt"))

user_id = sp.current_user()["id"]

song_uri = []
num = 0
for x in songs:
    if num < 100:
        print(x)
        result = sp.search(q=f"track:{x}year:{year}", type="track", limit=30)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uri.append(uri)
        except IndexError:
            print("song doesn't exist in spotify. skipped")
    num += 1

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
