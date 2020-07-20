from bs4 import BeautifulSoup 
import requests



header={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}

def get_html(artist,track):
    my_url = 'https://www.musixmatch.com/search/'+artist+' '+track
    print('Searching at : ' + my_url)

    
    page=requests.get(my_url, headers=header)
    soup= BeautifulSoup(page.content,'html.parser')
    titles = soup.findAll("a", class_= "title")
    
    print('Found lyric at URL : '+titles[0]['href'])
    

    return titles[0]['href']

def get_lyrics(artist,track):
    
    url_end = get_html(artist,track)
    my_url = 'https://www.musixmatch.com'+url_end

    page=requests.get(my_url, headers=header)
    soup= BeautifulSoup(page.content,'html.parser')
    lyrics = soup.findAll("p",class_='mxm-lyrics__content')
    out_lyric=""
    for lyric in lyrics:
        out_lyric+=(lyric.get_text())

    if(out_lyric==""):
        #& [0].get_text()=="Unfortunately we're not authorized to show these lyrics."
        test = soup.findAll("div",class_='empty-message')
        print(test[0].get_text())
        out_lyric='Restricted'


    #print(out_lyric)
    return out_lyric
    
