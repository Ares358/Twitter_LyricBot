import time
import datetime
import random
from os import environ
from PIL import Image
import requests
import io

from musixmatch_api_cleaner import *

import tweepy

key = environ['TWITTER_KEY']
secret = environ['TWITTER_SECRET']
BearerToken = environ['TWITTER_BearerToken']
access_token= environ['TWITTER_access_token']
access_token_secret = environ['TWITTER_access_token_secret']
api_key = environ['UNSPLASH_api_key']

auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

   
query=['Random','Tokyo life','Night city','flowers','Sea','Night sky','stars','Love','Moon','Film','Street Photography','Book','Friendship']


FILE_NAME = 'lastseen.txt'
FAV_FILE = 'Fav_list.txt'
HASH = '#getsnip'

def read_file(FILE):
    file_read = open(FILE, 'r')
    file_data = file_read.read().strip()
    file_read.close()
    return file_data



def store_lastseen(FILE_NAME, lastseen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(lastseen_id))
    file_write.close()
    return


def post_tweet():
    trackList = read_file(FAV_FILE)
    flag=0
    while(flag!=1):
        try:
            line = getLine(str(trackList))
            separator = line.find('-')
            track = line[:separator]
            artist= line[separator+1:]

            print(artist+' + '+track)

            if(artist==read_file('lastartist.txt')):
                continue

            n = len(artist)+len(track)+6
            msg = lyric_matcher(track,artist,n)
            if "Lyric not found" in msg:
                continue
            elif "Lyric too " in msg:
                continue

            msg += '\n'+get_track_artist(track,artist)
            print(msg)

#             no=0
#             while(True):
#                 no = random.randint(0,24)
#                 if(os.path.exists(str(no)+'.jpg')):
#                     break
#                 else:
#                     continue

#             print(str(no)+' exists')
#             api.update_with_media(str(no)+'.jpg', msg)
#             os.remove(str(no)+'.jpg')
#             print('Posted and deleted '+str(no))

            q = query[random.randint(0,len(query)-1)]
            call='https://api.unsplash.com/photos/random/?query='+q+'&content_filter=high&orientation=landscape&count=1&featured=true&client_id='+api_key
            request = requests.get(call)
            data = request.json()
            url = data[0]['urls']['full']

            img = Image.open(requests.get(url, stream=True).raw)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            api.update_with_media(file=img_byte_arr, msg)
            print('Posted and deleted '+str(no))

            flag=1

            store_lastseen('lastartist.txt',artist)

        except Exception as E:
            flag=0
            print("Duplicate status averted")
            print(E)
            continue


def reply():
    tweets = api.mentions_timeline(read_file(FILE_NAME),tweet_mode='extended')

    for tweet in reversed(tweets):
        if HASH in tweet.full_text.lower():

            store_lastseen(FILE_NAME, tweet.id)
            print(str(tweet.id) + "-" + tweet.full_text+ "\n\n")

            track_start = 9 + (tweet.full_text.lower().find(HASH))
            track_end = tweet.full_text.lower().find('by')
            track = tweet.full_text[track_start:track_end-1]
            artist = tweet.full_text[track_end + 3:]
            print(track)
            print(artist)
            n = len(artist)+len(track)+8+len(tweet.user.screen_name)
            msg = lyric_matcher(track,artist,n)
            print(msg)
            if "Lyric not found" in msg or "Peace out puny Human" in msg:
                api.update_status('@' + tweet.user.screen_name + '\n' + msg+"\nConsider re-checking the request format and spellings or requesting another track",tweet.id)
                continue
            msg += '\n'+get_track_artist(track,artist)
            api.retweet(tweet.id)
            api.create_favorite(tweet.id)

#             no=0
#             while(True):
#                 no = random.randint(0,24)
#                 if(os.path.exists(str(no)+'.jpg')):
#                     break
#                 else:
#                     continue

#             print(str(no)+' exists')
#             api.update_with_media(filename=str(no)+'.jpg',status ='@' + tweet.user.screen_name +'\n' + msg,in_reply_to_status_id=tweet.id)
#             os.remove(str(no)+'.jpg')
#             print('Posted and deleted '+str(no))
            q = query[random.randint(0,len(query)-1)]
            call='https://api.unsplash.com/photos/random/?query='+q+'&content_filter=high&orientation=landscape&count=1&featured=true&client_id='+api_key
            request = requests.get(call)
            data = request.json()
            url = data[0]['urls']['full']

            img = Image.open(requests.get(url, stream=True).raw)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            api.update_with_media(file=img_byte_arr,status ='@' + tweet.user.screen_name +'\n' + msg,in_reply_to_status_id=tweet.id)

        store_lastseen(FILE_NAME, tweet.id)



flag=[0]

def doThis(flag):
    now = datetime.datetime.now()
    hr = now.hour
    if(hr%3==0):
        if(flag[0]==0):
            post_tweet()
            flag[0]=1
    else:
        flag[0]=0
    reply()
    time.sleep(60)

while True:
    doThis(flag)


# i=0
# while True:
#     i+=1
#     i=i%179
#     reply()
#     if(i==1):
#        post_tweet()
#     time.sleep(60)

# track = 'Girls like you'
# artist = 'Denny'
# n = len(artist)+len(track)+8
# msg = lyric_matcher(track,artist,n)
# print(msg)
# if "Lyric not found" in msg:
#     print("Lyric not found lol")
# else:
#     msg += '\n'+get_track_artist(track,artist)
# print('\n----------------\n'+msg+'\n----------------\n')


