import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import simplejson as json
import pandas as pd
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
                    if json.loads(data)['place']['country'] == 'United States':
                        f.write(data)  # This will store the whole JSON data in the file, you can perform some JSON filters
                        twitter_text = json.loads(data)['text']  # You can also print your tweets here
                        print(twitter_text)
                        print()
                        self.num_tweets += 1
                        # Just to limit the number of tweets collected to check the
                        # program at the beginning, then increase the limit
                        if self.num_tweets < 10:
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
twitter_stream.filter(track=["news"])  # Add your keywords and other filters

print('_______ End _______')

# Create the CSV file
with open("MyFile.csv", 'a') as csv:
    # Write the title of the columns (features) that you want to store in the CSV file
    csv.write("id," + "created_at," + "text," + "country," + "followers," + "friends" + "\n")

    # Copy the data from the JSON file
    with open('MyFile.json', 'r') as jsonfile:
        for tweet in jsonfile:
            data = json.loads(tweet)


            # The int values should be converted to strings
                csv.write(str(data["id"]) + ",")
                csv.write(str(data["created_at"]) + ",")
                csv.write((str(data["text"]).replace("\n", "").replace(",", "")) + ",")
                csv.write(str(data["place"]["country"]) + ",")
                csv.write(str(data["user"]["followers_count"]) + ",")
                csv.write(str(data["user"]["friends_count"]))
                csv.write("\n")


tweets = pd.read_csv('MyFile.csv', index_col=0, encoding='ISO-8859-1')
tweets.head(100)

count = 0
for text in tweets.text:
    analysis = TextBlob(text)
    polarity = analysis.sentiment[0]
    subjectivity = analysis.sentiment[1]
    count += 1

print("Average Polarity:", polarity / count)
print("Average Subjectivity:", subjectivity / count)

text = tweets.text.values
wordcloud = WordCloud(
    width = 3000,
    height = 2000,
    background_color = 'black',
    stopwords = STOPWORDS).generate(str(text))
fig = plt.figure(
    figsize = (40, 30),
    facecolor = 'k',
    edgecolor = 'k')
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()