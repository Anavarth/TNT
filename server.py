import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import sys
class TwitterClient(object):
    def __init__(self):
        consumer_key = 'X0tBcqHUyEw4ff4r0gbKuUVMx'
        consumer_secret = 'MkKH8EQO0jJIagnp18SE8ObPaum2Drrw0lm4999rpaqgVdcWgh'
        access_token = '2878973166-29Ceyi2i1xZCh8f9D02tdlwHxW5Fn4xFotHNWZt'
        access_token_secret = '6LkjXnBJ0SrjV5JYtl7NXyH2AL1NF7bRNHMsE3Xn6fVFg'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'good'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'bad'
    def get_tweets(self, query, count = 10):
        tweets = []
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e)) 
def main():
	buf = ''
	api = TwitterClient()
	tweets = api.get_tweets(query = 'Trending News', count = 200)
	non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
	gtweets = [tweet for tweet in tweets if tweet['sentiment'] == 'good']
	buf = buf + 'Good news percentage: {} %'.format(100*len(gtweets)/len(tweets))
	#print("Good news percentage: {} %".format(100*len(gtweets)/len(tweets)))
	btweets = [tweet for tweet in tweets if tweet['sentiment'] == 'bad']
	buf = buf + '\nBad news percentage: {} %'.format(100*len(btweets)/len(tweets))
	#print("Bad news percentage: {} %".format(100*len(btweets)/len(tweets)))
	buf = buf + '\nNeutral news percentage: {} %'.format(100*(len(tweets) - len(btweets) - len(gtweets))/len(tweets))
	#print("Neutral news percentage: {} %".format(100*(len(tweets) - len(btweets) - len(gtweets))/len(tweets)))
	buf = buf + '\n\nGood news:\n'
	#print("\n\nGood news:")
	for tweet in gtweets[:1000]:
		#print(tweet['text'].translate(non_bmp_map))
		buf = buf + tweet['text'].translate(non_bmp_map)
	buf = buf + '\n\nBad news:\n'
	#print("\n\nBad news:")
	for tweet in btweets[:1000]:
		#print(tweet['text'].translate(non_bmp_map))
		buf = buf + tweet['text'].translate(non_bmp_map)
	return buf
import socket
s = socket.socket()         
print("Socket successfully created")
port = int(sys.argv[1])
s.bind(('', port))        
print("socket binded to %s" %(port))
s.listen(5) 
print("socket is listening")
while True:
	c,addr = s.accept()
	print('Got connection from',addr)
	print(c.recv(1024).decode('ascii'))
	buf = main()
	#c.send('News Fetched!!!'.encode())
	c.send(buf.encode())
	c.close()
