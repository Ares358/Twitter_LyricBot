import requests
import json
import random
import dotenv
import os
from lyric_scraper import *

dotenv.load_dotenv()

# musixmatch api base url
base_url = "https://api.musixmatch.com/ws/1.1/"

# your api key
api_key = os.getenv('MUSIXMATCH_api_key')

sp_chars= [".","'","/","?"]

glob_artist="lol"
glob_track=""


def getLine(list):
    
    no = (list.count('\n'))
    no = int(no)
    n=random.randint(1,no-1)
    start = find_nth(list,'\n',n)
    end = find_nth(list,'\n',n+1)
    line = list[start:end].replace('\n','')
    return line

def legacy_get_track_artist(track,artist):
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

def get_track_artist(track,artist,n):
        api_call = base_url+track_matcher+format_url+track_search_parameter+track+artist_search_parameter+artist
        request = requests.get(api_call+api_key)
        data = request.json()
        msg = ''
        if(data['message']['header']['status_code']==404):
            return 'Track not found'
        track = data['message']['body']['track']['track_name']
        artist = data['message']['body']['track']['artist_name']
        for i in sp_chars:
            track=track.replace(i,"")
            artist=artist.replace(i,"")
            
        track=track.replace('&','And')
        artist=artist.replace('&','And')

        glob_track=track
        glob_artist=artist
        
        msg='#'+track.replace(' ','')+' by #'+artist.replace(' ','')

        
        #print(msg)
        #print(glob_artist)
        #print(glob_track)
        lyrics='\n\n'+get_lyrics(glob_artist,glob_track)+'\n'
        #print(lyrics)
        
        if (lyrics=='\n\nRestricted\n'):
            lyrics='\n\n'+legacy_lyric_matcher(glob_artist,glob_track,n)+'\n'
        
        return snip(lyrics,n) + '\n' + msg
        
def legacy_lyric_matcher(track,artist,n):
        api_call = base_url+lyrics_matcher+format_url+track_search_parameter+track+artist_search_parameter+artist
        request = requests.get(api_call+api_key)
        data = request.json()
        
        if (data['message']['header']['status_code']==404):
            lyrics='Lyric not found!!! \nPlease check if the format and the spellings are correct!\n'
            return lyrics
        else:
            lyrics='\n\n'+data['message']['body']['lyrics']['lyrics_body']
        
        lyrics=lyrics.replace('...','')
        lyrics.replace('\n\n\n','\n\n')
        lyrics=lyrics.replace("******* This Lyrics is NOT for Commercial use *******","")
        
        return lyrics
        #return snip(lyrics,n) + '\n'+legacy_get_track_artist(track,artist)

def lyric_matcher(track,artist,n):
        ans=get_track_artist(track,artist,n)
        return ans

        #api_call = base_url+lyrics_matcher+format_url+track_search_parameter+track+artist_search_parameter+artist
        #request = requests.get(api_call+api_key)
        #data = request.json()
        #
        #if (data['message']['header']['status_code']==404):
        #    lyrics='Lyric not found!!! \nPlease check if the format and the spellings are correct!\n'
        #    return lyrics
        #else:
        #    lyrics='\n\n'+data['message']['body']['lyrics']['lyrics_body']
        #
        #lyrics=lyrics.replace('...','')
        #lyrics.replace('\n\n\n','\n\n')
        #lyrics=lyrics.replace("******* This Lyrics is NOT for Commercial use *******","")
        
        #if(exists == 'Not Found'):
        #    return 'Track not found'
        #print(exists)
        #print(glob_artist)
        #print(glob_track)
        #lyrics='\n\n'+get_lyrics(glob_artist,glob_track)
        #return snip(lyrics,n) + '\n'+exists

def find_nth(haystack, needle, n):
    
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start




def snip(lyrics,n):
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


# api methods
lyrics_matcher = "matcher.lyrics.get"
track_matcher = "matcher.track.get"


# format url
format_url = "?format=json&callback=callback"

# parameters
artist_search_parameter = "&q_artist="
track_search_parameter = "&q_track="
