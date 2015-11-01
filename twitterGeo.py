from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

#twitter credentials
access_token = "4071886992-bnHpHdKy7yOJVrnotHFs5APG1QC4gurgi9Gc5LU"
access_token_secret = "zfR4t6WM2Zmf5185uW3aJ6xxqnth8lwZYMoBNtvsPypDR"
consumer_key = "8uzP5HaulOr2a5z9WUOiegkqf"
consumer_secret = "DpfkvmXmcy23PReWBVZEUziFRSjo9ZxClMGY6MIpiTmtajl8cS"

f = open('data/twitter_data.txt', 'w')
hashtags = []

#twitter listener
class twitterListener(StreamListener):

    def on_data(self, data):
        decoded = json.loads(data)


        username = unicode(decoded['user']['screen_name']).encode("ascii","ignore")  #gets username
        userTweet = unicode(decoded['text'].encode('ascii', 'ignore')) #gets tweet
        userTweetTime = unicode(decoded['created_at']) #gets timestamp
        userLocation = unicode(decoded['user']['location']).encode("ascii","ignore")  #gets location
        userCoords = unicode(decoded['coordinates']) #gets coordinates

        userData = userTweetTime + " @" + username + ": " + userTweet + " Hashtags: "

        #Loops through the list of hashtags and adds them to userData
        userHashtags = decoded['entities']['hashtags']
        tmp = decoded['text']
        for Hashtags in userHashtags:
            userHashtags = Hashtags['text']
            userData += userHashtags
            
            
        userData += "\n"
        print userData

        f.write(userData)

        
       # userURLS = unicode(decoded['entities']['urls'])
        #print userHashtags
       # print userURLS
        
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #Authentication and connection to twitter API
    l = twitterListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream = Stream(auth, l)
    stream.filter(locations=[-122.75,36.8,-121.75,37.8]) #filter tweets to be in the San Francisco area
    f.close()