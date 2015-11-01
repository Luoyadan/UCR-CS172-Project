from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

#twitter credentials
access_token = "4071886992-bnHpHdKy7yOJVrnotHFs5APG1QC4gurgi9Gc5LU"
access_token_secret = "zfR4t6WM2Zmf5185uW3aJ6xxqnth8lwZYMoBNtvsPypDR"
consumer_key = "8uzP5HaulOr2a5z9WUOiegkqf"
consumer_secret = "DpfkvmXmcy23PReWBVZEUziFRSjo9ZxClMGY6MIpiTmtajl8cS"


#twitter listener
class twitterListener(StreamListener):

    def on_data(self, data):
        decoded = json.loads(data)

        if decoded.has_key('user'):
            username = unicode(decoded['user']['screen_name']) #gets username
            print username
            userTweet = unicode(decoded['text'].encode('ascii', 'ignore')) #gets tweet
            print userTweet
            userTweetTime = unicode(decoded['created_at']) #gets timestamp
            userLocation = unicode(decoded['user']['location']) #gets location
            #print userLocation
            userCoords = unicode(decoded['coordinates']) #gets coordinates
            print userCoords
            print "\n"

        '''
        userHashtags = unicode(decoded['entities']['hashtags'])
        userURLS = unicode(decoded['entities']['urls'])
        print userHashtags
        print userURLS
        '''
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    lat = 34.0422
    lng = -118.2437

    #Authentication and connection to twitter API
    l = twitterListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    tweets_data_path = '../data/twitter_data.txt'

    #Filters twitter search with 'programming'
    stream = Stream(auth, l)
    stream.filter(locations=[-122.75,36.8,-121.75,37.8]) #filter tweets to be in the San Francisco area