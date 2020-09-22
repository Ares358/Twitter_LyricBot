import time

from musixmatch_api_cleaner import *
import tweepy

dotenv.load_dotenv()

key = os.getenv('TWITTER_KEY')
secret = os.getenv('TWITTER_SECRET')
BearerToken = os.getenv('TWITTER_BearerToken')
access_token=os.getenv('TWITTER_access_token')
access_token_secret = os.getenv('TWITTER_access_token_secret')

auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

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
            print(msg)
            if "Lyric not found" in msg:
                continue
            elif "Lyric too " in msg:
                continue

            msg = lyric_matcher(track,artist,n) + '\n'+get_track_artist(track,artist)
            print(msg)
            api.update_status(msg)
            flag=1
            
            store_lastseen('lastartist.txt',artist)

        except Exception as E:
            flag=0
            print("Duplicate status averted" + E)



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
            if "Lyric not found" in msg:
                api.update_status('@' + tweet.user.screen_name + '\n' + msg+"\nConsider re-checking the request format and spellings or requesting another track",tweet.id)
                continue
            msg = lyric_matcher(track,artist,n) + '\n'+get_track_artist(track,artist)
            api.update_status('@' + tweet.user.screen_name +'\n' + msg,tweet.id)

        api.create_favorite(tweet.id)
        api.retweet(tweet.id)
        store_lastseen(FILE_NAME, tweet.id)


i=0
while True:
    i=i%180
    reply()
    if(i==0):
       post_tweet()
    time.sleep(60)
    i+=1

# track = 'asdasdasdasd'
# artist = 'asdasdasdasasd'
# n = len(artist)+len(track)+8
# msg = lyric_matcher(track,artist,n)
# print(msg)
# if "Lyric not found" in msg:
#     print("Lyric not found lol")
# else:
#     msg = lyric_matcher(track,artist,n) + '\n'+legacy_get_track_artist(track,artist)
# print('\n----------------\n'+msg+'\n----------------\n')

