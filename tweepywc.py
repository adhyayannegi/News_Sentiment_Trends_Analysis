import tweepy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

consumer_key = "fdK3zTcrBkysSiThxOdZiNgts"
consumer_secret = "W07P3EYJ2vGnIWhxa1qIMXT1AHj7WQNycjsCryXBqcxkNmUqhu"
access_token = "331376208-og6EbhlyYujoHq8xEFu0qjcMRIpqNgfw8DqlMDKs"
access_token_secret = "lBWeeU9zT2QaO6ljCFjq76NlRoLmLe24QP9L5f2Mztc5o"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Define a function that will take our search query, a limit of 1000 tweets by default, default to english language
# and allow us to pass a list of words to remove from the string
def tweetSearch(query, limit=200, language="en", remove=[]):
    # Create a blank variable
    text = ""

    # Iterate through Twitter using Tweepy to find our query in our language, with our defined limit
    # For every tweet that has our query, add it to our text holder in lower case
    for tweet in tweepy.Cursor(api.search, q=query, lang=language).items(limit):
        text += tweet.text.lower()

    # Twitter has lots of links, we need to remove the common parts of links to clean our data
    # Firstly, create a list of terms that we want to remove. This contains https & co, alongside any words in our remove list
    removeWords = ["https", "co"]
    removeWords += remove

    # For each word in our removeWords list, replace it with nothing in our main text - deleting it
    for word in removeWords:
        text = text.replace(word, "")

    # return our clean text
    return text


#Generate our text with our new function
#Remove all mentions of the name itself, as this will obviously be the most common!
search = tweetSearch("kajol", remove = ["kajol"])


wordcloud = WordCloud().generate(search)

#Plot the text with the lines below
plt.figure(figsize=(18,9))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()