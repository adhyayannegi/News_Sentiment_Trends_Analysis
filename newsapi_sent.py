import requests
import json
from textblob import TextBlob #For Sentiment Analysis
from wordcloud import WordCloud
from datetime import datetime, timedelta
from dateutil.parser import parse
import pprint
import pandas as pd
import os
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import translate
from google.cloud import language

from google.cloud.language import enums

from google.cloud.language import types

import nltk

path = "GCP_Cred.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
translate_client = translate.Client()
"""
import requests

url = ('https://newsapi.org/v2/top-headlines?'
       'country=in&'
       'apiKey=b47679242575481999ad97c0eb555092')
response = requests.get(url)
try:
    response.json()
except json.decoder.JSONDecodeError:
    print("N'est pas JSON")
"""
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='b47679242575481999ad97c0eb555092')


# define client variable
client = language.LanguageServiceClient()

def sentiment_list(query):


    past=str(parse((datetime.now()-timedelta(days=7)).strftime('%Y-%m-%d')))
    present=str(parse(datetime.now().strftime('%Y-%m-%d')))

    all_articles = newsapi.get_everything(q=query,language='en',from_param=past,to=present)
        ## convert from json to dataframe
    german = all_articles
    german = pd.DataFrame.from_dict(german)
    german.replace(to_replace=[None], value=np.nan, inplace=True)
    german = german.fillna(0)
    german = pd.concat([german.drop(['articles'], axis=1), german['articles'].apply(pd.Series)], axis=1)
    # german.head()

    # local list, will be saved for later
    sent_list = []

    # iterates through the all articles capture by the News API. The datatframe is called "results"

    for i, row in german.iterrows():
        # creates a dictionary to store the data capture in the loop
        sent_dict = {}

        # uses the types.Document() function to perform analysis on the text and store it
        content=german.get('description', 'content')[i]

        # Detects the sentiment of the text stored above
        analysis = TextBlob(content)

        # Assigns dictionary values for the URL, Title, Description, Sentiment, Magnitude, and Category
        sent_dict['URL'] = german.url[i]
        sent_dict['Title'] = german.title[i]
        sent_dict['Content'] = german.content[i]
        sent_dict['Sentiment'] = analysis.sentiment[0]
        sent_dict['Magnitude'] = analysis.sentiment[1]
        sent_dict['Description'] = german.description[i]
        # sent_dict['Category'] = german.category[i]
        # Appending the values in our dictionary to a list
        sent_list.append(sent_dict)

    # We want to use this list later, so we will return it
    return sent_list



# display(sent_list)

def choose_news(sent_list,keyword):
    # User selects type of articles
    # choice = input("Are you looking for positive or negative articles?  \n")

    # sorts list from highest to lowest (reverse=True) for the positive articles
    # if choice == 'positive':
    # sent_list = sorted(sent_list, key=lambda k: k['Sentiment'], reverse=True)

    # sorts list from lowest to highest for the negative articles
    # if choice == 'negative':
    # sent_list = sorted(sent_list, key=lambda k: k['Sentiment'])

    i = 0
    p = 0
    n = 0
    print('FETCHING ARTICLES USING NEWSAPI for: '+keyword)

    sent_list = sorted(sent_list, key=lambda k: k['Sentiment'], reverse=True)

    print('\nGenerally POSITIVE AND HIGHLY SUBJECTIVE articles:')
    print('________________________________________________________\n')

    for score in sent_list:

        if (score['Sentiment'] > 0.1 and score['Magnitude']>=0.4):
            i = i + 1
            print(u"{}. {}\nURL: {}\n\nDescription: {}\n\nContent: {}\n\nSentiment: {}\nSubjectivity: {}\n".format(i, score['Title'], score['URL'],
                                                                                        score['Description'],
                                                                                        score['Content'],
                                                                                        score['Sentiment'],
                                                                                        score['Magnitude']))

    if (i == 0):
        print("\nNo Articles to show in this category.")

    print('')
    i = 0

    print('Generally POSITIVE AND OBJECTIVE article:')
    print('___________________________________________________\n')

    for score in sent_list:

        if (score['Sentiment'] > 0.1 and score['Magnitude'] < 0.4):
            i = i + 1
            print(
                u"{}. {}\nURL: {}\n\nDescription: {}\n\nContent: {}\n\nSentiment: {}\nSubjectivity: {}\n".format(i, score['Title'], score['URL'],
                                                                                        score['Description'],
                                                                                        score['Content'],
                                                                                        score['Sentiment'],
                                                                                        score['Magnitude']))

    if (i == 0):
        print("\nNo Articles to show in this category.")

    print('')
    i = 0


    sent_list = sorted(sent_list, key=lambda k: k['Sentiment'], reverse=True)
    print('Generally NEUTRAL AND HIGHLY SUBJECTIVE article:')
    print('______________________________________________________\n')

    for score in sent_list:

        if (score['Sentiment'] < 0.1 and score['Sentiment'] > -0.05 and score['Magnitude']>=0.4):
            i = i + 1
            print(u"{}. {}\nURL: {}\n\nDescription: {}\n\nContent: {}\n\nSentiment: {}\nSubjectivity: {}\n".format(i, score['Title'], score['URL'],
                                                                                        score['Description'],
                                                                                        score['Content'],
                                                                                        score['Sentiment'],
                                                                                        score['Magnitude']))

    if (i == 0):
        print("\nNo Articles to show in this category.")

    print('')
    i = 0


    print('Generally NEUTRAL AND OBJECTIVE article:')
    print('________________________________________________\n')

    for score in sent_list:

        if (score['Sentiment'] < 0.1 and score['Sentiment'] > -0.05 and score['Magnitude'] < 0.4):
            i = i + 1

            print(
                u"{}. {}\nURL: {}\n\nDescription: {}\n\nContent: {}\n\nSentiment: {}\nSubjectivity: {}\n".format(i, score['Title'], score['URL'],
                                                                                        score['Description'],
                                                                                        score['Content'],
                                                                                        score['Sentiment'],
                                                                                        score['Magnitude']))


    if(i==0):
        print("\nNo Articles to show in this category.")

    print('')
    i = 0

    sent_list = sorted(sent_list, key=lambda k: k['Sentiment'])

    print('Generally NEGATIVE AND OBJECTIVE sentiment article:')
    print('_________________________________________________________\n')
    for score in sent_list:

        if (score['Sentiment'] <= -0.05 and score['Magnitude'] < 0.4):
            i = i + 1
            print(
                u"{}. {}\nURL: {}\n\nDescription: {}\n\nContent: {}\n\nSentiment: {}\nSubjectivity: {}\n".format(i, score['Title'], score['URL'],
                                                                                        score['Description'],
                                                                                        score['Content'],
                                                                                        score['Sentiment'],
                                                                                        score['Magnitude']))
    if(i==0):
        print("\nNo Articles to show in this category.")

    print('')
    i = 0


    print('Generally NEGATIVE AND HIGHLY SUBJECTIVE sentiment article:')
    print('___________________________________________________________________\n')
    for score in sent_list:

        if (score['Sentiment'] <= -0.05 and score['Magnitude']>=0.4):
            i = i + 1
            print( u"{}. {}\nURL: {}\n\nDescription: {}\n\nContent: {}\n\nSentiment: {}\nSubjectivity: {}\n".format(i, score['Title'], score['URL'],
                                                                                        score['Description'],
                                                                                        score['Content'],
                                                                                        score['Sentiment'],
                                                                                        score['Magnitude']))
    if(i==0):
        print("\nNo Articles to show in this category.")


def mine_results_content(sent_list,keyword,top_count):
    import re
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from collections import Counter
    # from sklearn.feature_extraction import stop_words

    import warnings
    warnings.filterwarnings('ignore')

    # english stop words from nltk package
    stopWords = stopwords.words('english')
    # adding stopwords manually

    man = ['said', 'news', 'new', 'could', 'trying', 'might','0', '5', '1', '2', '3', '4', '6',
           '7', '8', '9', '10', '11', '000', '12', '19', '2019'
                                                         'like', 'fitted', 'planned', 'recommend', 'recommends',
           'sought', 'indeed', 'monday', 'tuesday', 'wednesday', 'friday',
           'thursday', 'saturday', 'sunday', 'chars', 'amp', 'first',
           'second', 'third', 'fourth', 'fifth', 'hour', 'day', 'much'
                                                                'january', 'february', 'march', 'april', 'may', 'june',
           'il', 'see',
           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'vs']
    man.extend(keyword.split())
    # append stopwords
    stopWords.extend(man)
    # conversion to set
    stopWords = set(stopWords)

    # send to dataframe
    sent_list = pd.DataFrame.from_dict(sent_list)
    # manipulate the string data
    for i in range(len(sent_list)):
        # replace any non-letter, space, or digit character in the headlines.

        # sent_list.Title[i] = re.sub("\s+",' ', sent_list.Title[i].lower())

        # sent_list.Description[i] = re.sub(r'[^\w\s\d]',' ',sent_list.Description[i].lower())
        sent_list.Content[i] = re.sub("[^a-zA-Z]", " ", str(sent_list.Content[i]))
        try:
            sent_list.Content[i] = re.sub(r'[^\w\s\d]', ' ', sent_list.Content[i].lower())
        except:
            pass
        # replace sequences of whitespace with a space character.

        #  sent_list.Title[i] = re.sub("\s+",' ', sent_list.Title[i])
        #  sent_list.Description[i] = re.sub("\s+",' ', sent_list.Description[i])
        sent_list.Content[i] = re.sub("\s+", ' ', sent_list.Content[i])

    headlines = pd.DataFrame(sent_list.Content.astype(str))
    headlines = headlines.Content.str.cat()
    headlines = word_tokenize(headlines)

    remove_stopwords = []

    for i in range(len(headlines)):
        if headlines[i] not in stopWords:
            remove_stopwords.append(headlines[i])

    top_words = pd.Series(remove_stopwords).value_counts()[:top_count]
    top_words = top_words.sort_index()
    # print(top_words)
    fig1 = plt.figure()

    top_words.plot(kind='bar')
    plt.xticks(rotation=45, fontsize=12)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top Words in the Current Trending Articles based on Content for: ' + keyword)

    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()

    fig1.savefig('Outputs/Newsapi Trends/' + keyword + '_article_trends_' +str(datetime.now().strftime("%H%M_%d%h%Y"))+ '.png')

"""  #headline trends redundant
    # english stop words from nltk package
    stopWords = stopwords.words('english')
    # adding stopwords manually
    man = ['said', 'news', 'new', 'could', 'trying', 'might', '5', '1', '2', '3', '4', '6', '7', '8', '9', '10', '11',
           '000', '12', '19',
           '2019','0',
           'like', 'fitted', 'planned', 'recommend', 'recommends', 'sought', 'indeed',
           'monday', 'tuesday', 'wednesday', 'friday', 'thursday', 'saturday', 'sunday', 'il', 'see'
                                                                                               'first', 'second',
           'third', 'fourth', 'fifth'
                              'january', 'february', 'march', 'april', 'may', 'june',
           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','vs']
    # append stopwords
    man.extend(keyword.split())
    stopWords.extend(man)
    # conversion to set
    stopWords = set(stopWords)

    # send to dataframe
    sent_list = pd.DataFrame.from_dict(sent_list)
    # manipulate the string data
    for i in range(len(sent_list)):
        # replace any non-letter, space, or digit character in the headlines.

        # sent_list.Title[i] = re.sub("\s+",' ', sent_list.Title[i].lower())

        sent_list.Description[i] = re.sub(r'[^\w\s\d]', ' ', sent_list.Description[i].lower())
        # sent_list.content[i] = re.sub(r'[^\w\s\d]',' ',sent_list.content[i]
        # replace sequences of whitespace with a space character.

        #  sent_list.Title[i] = re.sub("\s+",' ', sent_list.Title[i])
        sent_list.Description[i] = re.sub("\s+", ' ', sent_list.Description[i])
    #  sent_list.Content[i] = re.sub("\s+",' ', sent_list.Content[i])

    headlines = pd.DataFrame(sent_list.Description.astype(str))
    headlines = headlines.Description.str.cat()
    headlines = word_tokenize(headlines)

    remove_stopwords = []

    for i in range(len(headlines)):
        if headlines[i] not in stopWords:
            remove_stopwords.append(headlines[i])


    top_words = pd.Series(remove_stopwords).value_counts()[:top_count]
    top_words = top_words.sort_index()
    # print(top_words)


    fig2=plt.figure();
    top_words.plot(kind='bar')
    plt.xticks(rotation=45, fontsize=12)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top Words in the Current Trending Articles based on Headlines for '+keyword)
    plt.show()

    fig2.savefig('Outputs/Newsapi Trends/' + keyword + '_headline_trends_'+str(datetime.now().strftime("%H%M_%d%h%Y"))+ '.png')
"""


def mine_results_wordcloud(sent_list,keyword):
    import re
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from collections import Counter
    # from sklearn.feature_extraction import stop_words

    import warnings
    warnings.filterwarnings('ignore')

    # english stop words from nltk package
    stopWords = stopwords.words('english')
    # adding stopwords manually
    man = ['said', 'news', 'new', 'could', 'trying', 'might', '5', '1', '2', '3', '4', '6', '7', '8', '9', '10', '11',
           '000', '12', '19',
           '2019','0',
           'like', 'fitted', 'planned', 'recommend', 'recommends', 'sought', 'indeed',
           'monday', 'tuesday', 'wednesday', 'friday', 'thursday', 'saturday', 'sunday', 'il', 'see'
                                                                                               'first', 'second',
           'third', 'fourth', 'fifth'
                              'january', 'february', 'march', 'april', 'may', 'june',
           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','vs']
    # append stopwords
    man.extend(keyword.split())
    stopWords.extend(man)
    # conversion to set
    stopWords = set(stopWords)

    # send to dataframe
    sent_list = pd.DataFrame.from_dict(sent_list)
    # manipulate the string data
    for i in range(len(sent_list)):
        # replace any non-letter, space, or digit character in the headlines.

        # sent_list.Title[i] = re.sub("\s+",' ', sent_list.Title[i].lower())

        sent_list.Description[i] = re.sub(r'[^\w\s\d]', ' ', sent_list.Description[i].lower())
        # sent_list.content[i] = re.sub(r'[^\w\s\d]',' ',sent_list.content[i]
        # replace sequences of whitespace with a space character.

        #  sent_list.Title[i] = re.sub("\s+",' ', sent_list.Title[i])
        sent_list.Description[i] = re.sub("\s+", ' ', sent_list.Description[i])
    #  sent_list.Content[i] = re.sub("\s+",' ', sent_list.Content[i])

    headlines = pd.DataFrame(sent_list.Description.astype(str))
    headlines = headlines.Description.str.cat()
    headlines = word_tokenize(headlines)

    remove_stopwords = []

    for i in range(len(headlines)):
        if headlines[i] not in stopWords:
            remove_stopwords.append(headlines[i])



    #wordcloud = WordCloud().generate(text)

    # Plot the text with the lines below

    text = " ".join(remove_stopwords)
    time = datetime.now().strftime("Time: %H:%M  Date: %d-%m-%y")
    x, y = np.ogrid[:600, :600]

    mask = (x - 300) ** 2 + (y - 300) ** 2 > 260 ** 2
    mask = 255 * mask.astype(int)

    wc = WordCloud(background_color="black", repeat=True, mask=mask)
    wc.generate(text)

    fig2 = plt.figure()
    plt.text(1, 0.5, "WordCloud for: '" + keyword + "'\n" + time + '\n', fontsize=12)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()
    fig2.savefig('Outputs/Wordclouds/' + keyword + '_WordCloud_NewsAPI_' +str(datetime.now().strftime("%H%M_%d%h%Y"))+ '.png')


def driver_sentiment(keyword):
    sent_list = sentiment_list(keyword)
    choose_news(sent_list,keyword)

def driver_trends(keyword,top_count):
    sent_list = sentiment_list(keyword)
    mine_results_content(sent_list,keyword,top_count)

def driver_wordcloud(keyword):
    sent_list = sentiment_list(keyword)
    mine_results_wordcloud(sent_list, keyword)

#driver_sentiment('ajax')
#driver_trends('premier league',30)
#driver_wordcloud('liverpool')



