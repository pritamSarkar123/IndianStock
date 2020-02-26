import sys,tweepy,csv,re
from textblob import TextBlob

def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

def cleanTweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


def sentiment_analysis(searchTerm,NoOfTerms):
    tweetText = []
    consumerKey = '7jviSDTrCh3w41vlQOjix6cx1'
    consumerSecret = 'XUlJB8rGsDofF1H57MANZVOHjEcsamoiVCb5PjnBU4xrWa0jYO'
    accessToken = '751371062114390016-K5ksalxqwIb6qp7qbd0ARQAHfqMTTKo'
    accessTokenSecret = 'fOlmfNhbFpa5ElOLwGqQbahUy9r7ZWGBaOmumqHc2HJkw'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    # input for term to be searched and how many tweets to search
    #searchTerm = input("Enter Keyword/Tag to search about: ")
    #NoOfTerms = int(input("Enter how many tweets to search: "))

    # searching for tweets
    tweets=tweepy.Cursor(api.search, q=searchTerm,lang = "en").items(NoOfTerms)

    polarity = 0
    positive = 0
    negative = 0
    nutral = 0
    for tweet in tweets:
        tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity
        if (polarity == 0):
              nutral += 1
        if (analysis.sentiment.polarity > 0):
              positive += 1
        if (analysis.sentiment.polarity < 0):
              negative += 1

    positive = percentage(positive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    nutral = percentage(nutral, NoOfTerms)
    #print("P,Ne,Nu "+positive,negative,nutral)

    return positive,negative,nutral

#positive,negative,nutral=sentiment_analysis("moneycontrol",100)
#print(positive,negative,nutral)