import tweepy
import simplejson as json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from textblob import TextBlob

# Complete with your keys

consumer_key = '8LbgPJVK5AgR1vKcvCssNyKkp'
consumer_secret = 'PPrIa7y3xcK4aktfqqEUeQuk2K8BzwmYsXoBZkmCaVygqW3J9M'
access_token = '191181457-zejYmLuj85d5XOzRxNX2tFIncNvqIEwnhqmzVjCb'
access_secret = 'LfQ7P7I1e47as04eptD2er246ZmJdhkQiLol6ARkC6nTP'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)


class MyListener(StreamListener):

    def __init__(self, api=None):
        super(StreamListener, self).__init__()
        self.num_tweets = 0

    def on_data(self, data):
        try:
            with open('MyFile.json', 'a') as f:
                if json.loads(data).get('place'):
                    # if json.loads(data)['place']['country'] == 'United States':
                    f.write(data)  # This will store the whole JSON data in the file, you can perform some JSON filters
                    twitter_text = json.loads(data)['text']  # You can also print your tweets here
                    print(twitter_text)
                    print()
                    self.num_tweets += 1
                    # Just to limit the number of tweets collected to check the
                    # program at the beginning, then increase the limit
                    if self.num_tweets < 250:
                        return True
                    else:
                        return False
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print('Error :', status.place)
        return False


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=["covid"], languages=['en'])  # Add your keywords and other filters

print('_______ End _______')