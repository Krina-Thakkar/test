import requests 
from bs4 import BeautifulSoup 
import re
import pandas as pd
import numpy as np
from time import sleep
from flask import Flask,render_template,url_for,request
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

def scrape(k):
    print("Hello")
    URL = "https://www.musixmatch.com/explore"
    headers = {'Accept': 'text/html'}
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup_level1=BeautifulSoup(response.content, 'html.parser')
    songs_list= []
    for link in soup_level1.find_all('a', href=re.compile("/lyrics//*")):
        songs_list.append("https://www.musixmatch.com" + link.get('href'))
    print(songs_list)
    complete_list = []
    for song in songs_list:
        song_response = requests.get(song, headers={'User-Agent': 'Mozilla/5.0'})
        #sleep(2)
        print(song_response.status_code)
        soup = BeautifulSoup(song_response.content, 'html.parser')
        title = soup.find('h1', {'class':'mxm-track-title__track '})
        print(title)
        title = title.contents[1]
        lyrics = ''
        for lyric in soup.find_all('span', {'class':'lyrics__content__ok'}):
            lyrics+=lyric.contents[0]
        artist = soup.find('a', {'class':'mxm-track-title__artist mxm-track-title__artist-link'})
        artist = artist.contents[0]
        complete_list.append((title,artist,lyrics))
    df = pd.DataFrame(complete_list, columns=['title', 'artist', 'lyrics'])
    return df[:k]
    
def song_classifier(scr):
    NB_spam_model = open('C:\\Users\\Yash Lekhwani\\lyrics_clf_1000_py27.pkl','rb')
    clf = joblib.load(NB_spam_model)
    print(type(scr))
    my_prediction = clf.predict(scr['lyrics'].values)
    scr['Predictions'] = my_prediction
    probas_ = clf.predict_proba(scr['lyrics'].values)
    scr['Probability'] = np.around(probas_[:,1] * 100,2) 
    return scr
