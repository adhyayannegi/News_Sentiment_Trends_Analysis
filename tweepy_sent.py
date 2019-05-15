import tweepy #The Twitter API
from tkinter import * #For the GUI
from time import sleep
from wordcloud import WordCloud
from datetime import datetime
from textblob import TextBlob #For Sentiment Analysis
import matplotlib.pyplot as plt #For Graphing the Data
import logging
from datetime import datetime, timedelta
from dateutil.parser import parse
import csv
import newsapi_sent as newsapisent
import numpy as np

f = open('en.csv')
csv_f = csv.reader(f)
cuss_words=[]
for row in csv_f:
    cuss_words.extend(row)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # process everything, even if everything isn't printed

ch = logging.StreamHandler()
ch.setLevel(logging.INFO) # or any other level
logger.addHandler(ch)

#twwepy credentials

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
quote=""
root = Tk()
root.title("News Analysis")
#root.geometry("280x160") #You want the size of the app to be 500x500
#root.resizable(0, 0) #Don't allow resizing in the x or y direction


label1 = Label(root, text="Enter keyword for news/tweets")
E1 = Entry(root, bd =5)

label2 = Label(root, text="No. of Tweets (max. 1000)")
E2 = Entry(root, bd =5)

label3=Label(root, text="No. of Top Trends (max. 25)")
E3 = Entry(root, bd =5)

def getE1():
    return E1.get()

def getE2():
    return E2.get()

def getE3():
    return E3.get()


def getNewsapiSentiment():
    getE1()
    keyword = getE1()
    newsapisent.driver_sentiment(keyword)


def getTrendsNewsAPI():
    getE1()
    keyword = getE1()

    getE3()
    top_trends= getE3()
    top_trends = int(top_trends)
    newsapisent.driver_trends(keyword,top_trends)



def getWordCloudNewsAPI():
    getE1()
    keyword = getE1()
    newsapisent.driver_wordcloud(keyword)


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def getSentiment():
    getE1()
    keyword = getE1()

    getE2()
    numberOfTweets = getE2()
    numberOfTweets = int(numberOfTweets)
    public_tweets = api.search(keyword, 'en')
    count=0;
    #print("\nFetching Top 20 Tweets for keyword:'"+keyword+"'\n")
    quote="\nFetching Top 20 Tweets for keyword:'"+keyword+"'\n...\n\n"
    for tweet in tweepy.Cursor(api.search, keyword, 'en').items(numberOfTweets):
            count=count+1;
            #print("Tweet:"+str(count)+"=>\n"+tweet.text)
            quote+="Tweet:"+str(count)+"=>\n"+tweet.text
            analysis = TextBlob(tweet.text)

            #print(analysis.sentiment)
            quote+=("\n"+str(analysis.sentiment))
            if analysis.sentiment[0] > 0.2:
                #print('GENERALLY POSTITIVE SENTIMENT\n')
                quote+='\nGENERALLY POSTITIVE SENTIMENT\n\n'
            elif analysis.sentiment[0] < 0:
                #print('GENERALLY NEGATIVE ENTIMENT\n')
                quote += '\nGENERALLY NEGATIVE SENTIMENT\n\n'
            else:
                #print('GENERALLY NEUTRAL SENTIMENT\n')
                quote += '\nGENERALLY NEUTRAL SENTIMENT\n\n'

            if count==20:
                break;

    print(quote)
    polarity_list = []
    numbers_list = []
    number = 1

    for tweet3 in tweepy.Cursor(api.search, keyword, lang="en").items(numberOfTweets):
        try:
            analysis = TextBlob(tweet3.text)
            analysis = analysis.sentiment
            polarity = analysis.polarity
            polarity_list.append(polarity)
            numbers_list.append(number)
            number = number + 1

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break

    #Plotting
    fig1 = plt.figure()

    axes = plt.gca()
    axes.set_ylim([-1, 2])

    plt.scatter(numbers_list, polarity_list)

    averagePolarity = (sum(polarity_list))/(len(polarity_list))
    averagePolarity = "{0:.0f}%".format(averagePolarity * 100)

    time = datetime.now().strftime("Time: %H:%M  Date: %d-%m-%y")

    plt.text(0, 1.25, "Average Sentiment:  " + str(averagePolarity) + "\n" + time, fontsize=12, bbox = dict(facecolor='none', edgecolor='black', boxstyle='square, pad = 1'))

    plt.title("Sentiment of '" + keyword + "' on Twitter")
    plt.xlabel("Number of Tweets")
    plt.ylabel("Sentiment")
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()
    fig1.savefig('Outputs/Sentiment Graphs/'+keyword+'_SentimentGraph_'+str(datetime.now().strftime("%H%M_%d%h%Y"))+'.png')
    #plt.close()

    # Iterate through Twitter using Tweepy to find our query in our language, with our defined limit
    # For every tweet that has our query, add it to our text holder in lower case


def getWordCloudTwitter():
    getE1()
    keyword = getE1()

    getE2()
    numberOfTweets = getE2()
    numberOfTweets = int(numberOfTweets)

    text = ""
    for tweet2 in tweepy.Cursor(api.search, keyword, 'en').items(numberOfTweets):
        text += tweet2.text.lower()

    # Twitter has lots of links, we need to remove the common parts of links to clean our data
    # Firstly, create a list of terms that we want to remove. This contains https & co, alongside any words in our remove list
    removeWords = ["https", "co",keyword]
    removeWords.extend(cuss_words)

    # For each word in our removeWords list, replace it with nothing in our main text - deleting it
    for word in removeWords:
        text = text.replace(word, "")

    #text=''.join(unique_list(text.split()))
        # return our clean text
    # Generate our text with our new function
    # Remove all mentions of the name itself, as this will obviously be the most common!

    wordcloud = WordCloud().generate(text)
    time = datetime.now().strftime("Time: %H:%M  Date: %d-%m-%y")
    # Plot the text with the lines below
    fig2 = plt.figure()
    plt.text(1, 0.5, "WordCloud for: '" + keyword+"'\n" + time+'\n', fontsize=12)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()
    fig2.savefig('Outputs/Wordclouds/' + keyword + '_WordCloud_Twitter_'+str(datetime.now().strftime("%H%M_%d%h%Y"))+ '.png')



# Define a function that will take our search query, a limit of 1000 tweets by default, default to english language
# and allow us to pass a list of words to remove from the string
# def tweetSearch(query, limit, language="en", remove=[]):
# Create a blank variable


submit1 = Button(root, text ="Sentiment Analysis using NewsAPI", command = getNewsapiSentiment)
submit2=  Button(root, text ="NewsAPI Top Trends", command = getTrendsNewsAPI)
submit3 = Button(root, text ="NewsAPI Word Cloud", command = getWordCloudNewsAPI)
submit4 = Button(root, text ="Sentiment Analysis and Graph using Twitter API", command = getSentiment)
submit5 = Button(root, text ="Twitter Word Cloud", command = getWordCloudTwitter)


label1.pack()
E1.pack()
label2.pack()
E2.pack()
label3.pack()
E3.pack()

submit1.pack(padx=(10,10),pady=(10,5))
submit2.pack(pady=(3,5))
submit3.pack(pady=(3,5))
submit4.pack(pady=(10,5))
submit5.pack(pady=(3,5))
#root2 = Tk()


root.mainloop()
#root2.mainloop()
