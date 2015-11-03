import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import argparse

import json
import urllib2
from lxml.html import parse


#arguments
dirName = str(sys.argv[1])
'''
boundLat1 = float(sys.argv[2])
boundLong1 = float(sys.argv[3])
boundLat2 = float(sys.argv[4])
boundLong2 = float(sys.argv[5])
'''

#twitter credentials
access_token = "4071886992-bnHpHdKy7yOJVrnotHFs5APG1QC4gurgi9Gc5LU"
access_token_secret = "zfR4t6WM2Zmf5185uW3aJ6xxqnth8lwZYMoBNtvsPypDR"
consumer_key = "8uzP5HaulOr2a5z9WUOiegkqf"
consumer_secret = "DpfkvmXmcy23PReWBVZEUziFRSjo9ZxClMGY6MIpiTmtajl8cS"

tweetcnt = 0
filecnt = 0
outputPath = dirName
outputPath += '/'
outputPath += 'twitter_data'
outputPath += str(filecnt)
outputPath += '.txt'
f = open(outputPath, 'w')
hashtags = []


#twitter listener
class twitterListener(StreamListener):
    

    def on_data(self, data):
        global f
        global filecnt
        global tweetcnt

        #Create a new text file every 10MB
        if (f.tell() >= 10485760):
            f.close()
            filecnt += 1
            outputPath = dirName
            outputPath += '/'
            outputPath += 'twitter_data'
            outputPath += str(filecnt)
            outputPath += '.txt'
            f = open(outputPath, 'w')

        
        decoded = json.loads(data)  

        #Checks geo enable and if there is coordinates
        if unicode(decoded['user']['geo_enabled']).encode("ascii","ignore") == "True" and unicode(decoded['coordinates']).encode("ascii","ignore") != "None":

            username = unicode(decoded['user']['screen_name']).encode("ascii","ignore")  #gets username
            userTweet = unicode(decoded['text']).encode("ascii","ignore") #gets tweet
            userTweetTime = unicode(decoded['created_at']) #gets timestamp
            userLocation = unicode(decoded['user']['location']).encode("ascii","ignore") #gets location as per profile, not of the specific tweet
            userCoords = unicode(decoded['coordinates']).encode("ascii","ignore") #gets coordinates, will be 'None' if they have disable location services
            userURLS = unicode(decoded['entities']['urls']).encode("ascii","ignore")#get URLS 
            userData = userTweetTime +  " Coords: " + userCoords[36:-1] + " @" + username + ": " + userTweet + " Hashtags: " 

            #Loops through the list of hashtags and adds them to userData
            userHashtags = decoded['entities']['hashtags']
            tmp = decoded['text']
            for Hashtags in userHashtags:
                userHashtags = Hashtags['text']
                userData += userHashtags + " "
            
            #url
            if userURLS != "[]":
                expanded_url = unicode(decoded['entities']['urls'][0]['expanded_url']).encode("ascii","ignore")
                userData += " URL: "
                userData += expanded_url
                
                try:
                    page = urllib2.urlopen(expanded_url)
                    p = parse(page)
                    pageTitle = p.find(".//title").text.encode("ascii","ignore")
                    userData += " Page-title: " 
                    userData += pageTitle
                except urllib2.HTTPError, err:
                    if err.code == 404:
                        print "Page not found!"
                    elif err.code == 403:
                        print "Access denied!"
                    else:
                        print "Error:", err.code
                except urllib2.URLError, err:
                    print "URL error:", err.reason
        
            tweetcnt += 1
            print 'Tweet:', tweetcnt, ' F.size = ', f.tell(), ' on file:', filecnt 
            userData += "\n"
            print userData
            f.write(userData)

        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    
    #Authentication and connection to twitter API
    l = twitterListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #-122.75,36.8,-121.75,37.8 SF
    #stream.filter(locations=[boundLong1,boundLat1,boundLong2,boundLat2], languages=["en"]) #filter tweets to be in the San Francisco area
    #stream.filter(locations=[-121.32,32.64,-113.76,36.09], languages=["en"]) #filter tweets to be in the Southern Califnornia area
    stream.filter(locations=[-123.40,35.59,-66.79,48.25], languages=["en"]) 

    f.close()
