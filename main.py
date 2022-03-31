from selenium.webdriver.common.by import By
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os


URL ="https://www.billboard.com/charts/hot-100/"

#date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
date = "1998-09-01"
URL_with_date = f"{URL}{date}"

driver = webdriver.Chrome(executable_path="C:\\Users\\MAXMEDIA\\Desktop\\Python downloads\\Chromedriver\\chromedriver.exe")
driver.get(URL_with_date)
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
time.sleep(2)
html_code = driver.page_source

#print(html_code)

soup = BeautifulSoup(html_code, "html.parser") #this is an object containing parsed data, which is searchable/callble through BS4 methods
first_track = soup.find(name="a", class_="c-title__link lrv-a-unstyle-link").getText().lstrip().rstrip()
tracks_pre = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
tracks = []
tracks.append(first_track)

for track in tracks_pre:
    new_track = track.text.lstrip().rstrip()
    tracks.append(new_track)

#print(tracks)

client_id = os.environ["client_id"]
client_secret = os.environ["client_secret"]
username = "zfbawx4xb5rcgpklomof5kapl"

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri="http://example.com", client_id=client_id, client_secret=client_secret, scope=scope))

results = sp.current_user()
print(results)

uris_list = [f"track:{track}"for track in tracks]

print(uris_list)

#create = sp.user_playlist_create(user=username, name=f"{date} Billboard 100", public=True, collaborative=False)
#print(create)
playlist_id = "51lN8okGMSrq9p9BxsQ2Oc" #MAKE THIS NOT HARD CODED
#sp.playlist_add_items(playlist_id=playlist_id, items=uris_list)
new_uri_list = []
for name in uris_list:
    try:
        song = sp.search(q=name, type="track")
        uri = song["tracks"]["items"][0]["uri"]
    except IndexError:
        pass
    else:

        print(uri)
        new_uri_list.append(uri)
        #print(song)
        pass

print(new_uri_list)
sp.playlist_add_items(playlist_id=playlist_id, items=new_uri_list)