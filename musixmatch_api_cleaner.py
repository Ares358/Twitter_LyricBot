import requests
import json
import random
from os import environ

# musixmatch api base url
base_url = "https://api.musixmatch.com/ws/1.1/"

# your api key
api_key =environ['MUSIXMATCH_api_key']

sp_chars= [".","'","/","?","#",'@',"'",',','/','-']

# api methods
lyrics_matcher = "matcher.lyrics.get"
track_matcher = "matcher.track.get"


# format url
format_url = "?format=json&callback=callback"

# parameters
artist_search_parameter = "&q_artist="
track_search_parameter = "&q_track="


def find_nth(haystack, needle, n):
    """Find the nth occurrence of substring in a string."""
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def getLine(list):
    """Get line from list iterator."""
    no = (list.count('\n'))
    no = int(no)
    n=random.randint(1,no-1)
    start = find_nth(list,'\n',n)
    end = find_nth(list,'\n',n+1)
    line = list[start:end].replace('\n','')
    return line

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

def get_track_artist(track,artist):
    """Get track artist detail."""
    for i in sp_chars:
        track=track.replace(i,"")
        artist=artist.replace(i,"")

    api_call = base_url+track_matcher+format_url+track_search_parameter+track+artist_search_parameter+artist
    request = requests.get(api_call+api_key)
    data = request.json()
    track = data['message']['body']['track']['track_name']
    artist = data['message']['body']['track']['artist_name']

    for i in sp_chars:
        track=track.replace(i,"")
        artist=artist.replace(i,"")

    track=track.replace('&','And')
    artist=artist.replace('&','And')
    msg='#'+track.replace(' ','')+' by #'+artist.replace(' ','')

    return msg

def lyric_matcher(track,artist,n):
    """Get the lyrics for track based on title and artist"""
    for i in sp_chars:
        track=track.replace(i,"")
        artist=artist.replace(i,"")
    api_call = base_url+lyrics_matcher+format_url+track_search_parameter+track+artist_search_parameter+artist
    request = requests.get(api_call+api_key)
    data = request.json()

    if (data['message']['header']['status_code']==404):
        lyrics='Lyric not found!!!\n'
        return lyrics
    else:
        lyrics='\n\n'+data['message']['body']['lyrics']['lyrics_body']

    lyrics=lyrics.replace('...','')
    lyrics.replace('\n\n\n','\n\n')
    lyrics=lyrics.replace("******* This Lyrics is NOT for Commercial use *******","")
    
    return snip(lyrics,n)

def snip(lyrics,n):
    """Get the snippet for a given track lyrics."""
    no=lyrics.count('\n\n')
    flag=0
    i=0
    while(flag!=1):
        flag=1
        n=random.randint(1,no)
        start = find_nth(lyrics,'\n\n',n)
        end = find_nth(lyrics,'\n\n',n+1)
        snippet = lyrics[start:end].replace('\n\n','')

        if(i>=no):
            if len(snippet)+n > 240:
                end = start+ find_nth(lyrics[start:],'\n',6)
                snippet = lyrics[start:end].replace('\n\n','')
                if len(snippet)+n > 240:
                    end = start+ find_nth(lyrics[start:],'\n',5)
                    snippet = lyrics[start:end].replace('\n\n','')
                    if len(snippet)+n > 240:
                        end = start+ find_nth(lyrics[start:],'\n',4)
                        snippet = lyrics[start:end].replace('\n\n','')
                        if len(snippet)+n > 240:
                            end = start+ find_nth(lyrics[start:],'\n',3)
                            snippet = lyrics[start:end].replace('\n\n','')
                            if len(snippet)+n > 240:
                                end = start+ find_nth(lyrics[start:],'\n',2)
                                snippet = lyrics[start:end].replace('\n\n','')
                                if len(snippet)+n > 240:
                                    snippet = 'Lyric too long to print. Consider requesting another song!!!\nPeace out puny Human!'
            elif len(snippet) < 70:
                end = start+ find_nth(lyrics[start:],'\n',1)
                snippet = lyrics[start:end].replace('\n\n','')
                if len(snippet) < 70:
                    end = start+ find_nth(lyrics[start:],'\n',2)
                    snippet = lyrics[start:end].replace('\n\n','')
                    if len(snippet) < 70:
                        end = start+ find_nth(lyrics[start:],'\n',3)
                        snippet = lyrics[start:end].replace('\n\n','')
                        if len(snippet) < 70:
                            end = start+ find_nth(lyrics[start:],'\n',4)
                            snippet = lyrics[start:end].replace('\n\n','')
                            if len(snippet) < 70:
                                end = start+ find_nth(lyrics[start:],'\n',5)
                                snippet = lyrics[start:end].replace('\n\n','')
                                if len(snippet) < 70:
                                    snippet = 'Lyric too small to print. Consider requesting another song!!!\nPeace out puny Human!'

        if len(snippet) < 70 or len(snippet)+n > 240:
            flag=0
            i+=1
    return snippet
