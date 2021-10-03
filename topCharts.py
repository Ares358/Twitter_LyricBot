import requests
import json
import random
from os import environ

# musixmatch api base url
base_url = "https://api.musixmatch.com/ws/1.1/"

def topCharts():
    api_key =environ['MUSIXMATCH_api_key']
    track_matcher = "chart.tracks.get"
    format_url = "?format=json&callback=callback"
    chart_name='&chart_name=hot'
    page='&page=1'
    page_size = '&page_size=100'
    country = '&country=us'
    has_lyrics = '&f_has_lyrics=1'

    api_call = base_url+track_matcher+format_url+chart_name+page+page_size+country+has_lyrics
    request = requests.get(api_call+api_key)
    data = request.json()

    track_list = data['message']['body']['track_list'] 

    tracks = []
    for track in track_list:
        track_name=track['track']['track_name']
        artist_name=track['track']['artist_name']
        tracks.append(track_name+'-'+artist_name)

    return tracks

# tracks = topCharts()
# for a in tracks:
#     print(a)
