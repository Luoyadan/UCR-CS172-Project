import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import argparse
import json
import urllib2
from lxml.html import parse
import time
import re

#arguments

dirName = str(sys.argv[2]) #data path
numTweets = int(sys.argv[1]) #num of tweets 
tweetcnt = 0
filecnt = 0
outputPath = dirName+ '/'+'data'+str(filecnt)+'.txt'
f = open(outputPath, 'a')
crawlerFlag = True


def get_verificationAndRun():
	
	#twitter credentials
	access_token = "781222791936811009-cGSYGEOBiNav8d4H4JbNdafTHwfhlMX"
	access_token_secret = "4EPQtdYAUiweWsmHHg5qQDaA6gB7USDVZ7kovXbyi7eVo"
	consumer_key = "edw09KDJ7XymoOhCwYxX8ifaV"
	consumer_secret = "4aVewZov2J4iuwAmIhfbohQ6vsmuD9z7UHTne31234CBCqb874"
	l = twitterListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	#tweets from areas between [-121.32,32.64] and [-73,41]
	stream.filter(locations=[-121.32,32.64,-73,41],languages=["en"]) 
	return
	
#twitter listener
class twitterListener(StreamListener):

	def __init__(self, api=None):
		super(twitterListener, self).__init__()
		self.numTweets = 0

	def on_data(self, data):
		global f
		global filecnt
		global tweetcnt
		global crawlerFlag
		#checks num of tweet parameter
		if tweetcnt >= numTweets and numTweets != 0:
			print "first"
			crawlerFlag = False
			return False

		#Ends when files reach 5GB in total size
		#finally , these data will be stored in Distributed file system HDFS (using .sh)
		if (filecnt >= 500):
			print "filecnt"
			crawlerFlag = False
			return False

		#Create a new text file every 10MB
		if (f.tell() >= 10*1024*1024):
			print "last"
			f.close()
			crawlerFlag= True
			filecnt += 1
			outputPath = dirName+'/'+'data'+str(filecnt)+".txt"
			f = open(outputPath, 'a')
        
		decoded = json.loads(data)
		#name and tweettime can be used to data cleaning
		username = unicode(decoded['user']['screen_name']).encode("ascii","ignore")  #gets username
		userId=unicode(decoded['id']).encode("ascii","ignore") 
		userTweet = unicode(decoded['text']).encode("ascii","ignore") #gets tweet
		userTweet = userTweet.replace('\n', ' ').replace('\t', '').replace('\r', '') #replaces new lines
		userFavor =	unicode(decoded['favorited']).encode("ascii","ignore")
		userTweetTime = unicode(decoded['created_at']) #gets timestamp
		userLocation = unicode(decoded['user']['location']).encode("ascii","ignore") #gets location as per profile, not of the specific tweet
		userCoords = unicode(decoded['coordinates']).encode("ascii","ignore") #gets coordinates, will be 'None' if they have disable location services
		userURLS = unicode(decoded['entities']['urls']).encode("ascii","ignore")#get URLS 
		userData = "Date:" + userTweetTime +  " Coords:" + userCoords[36:-1] +"Placs:"+userLocation+ " User:" + username +" UserId: "+userId + " Text:" + userTweet+" Favor: "+userFavor
		
		#get title if exists.
		pageTitle = None
		userData += " URL:"
		if userURLS != "[]":
			expanded_url = unicode(decoded['entities']['urls'][0]['expanded_url']).encode("ascii","ignore")
			userData += expanded_url

			try:
				page = urllib2.urlopen(expanded_url)
				p = parse(page)
				pageT = p.find(".//title")
				if (pageT != None):
				    pageTitle = unicode(p.find(".//title").text).encode("ascii","ignore")
			except urllib2.HTTPError, err:
				print "Error:", err.code
			except urllib2.URLError, err:
				print "URL error:", err.reason
			except UnicodeDecodeError:
				pass
			except IOError:
				pass
		else:
			userData+="None"
		userData += " Title:"
		if (pageTitle != None):
			pageTitle = re.sub('[^A-Za-z0-9]+', ' ', pageTitle)
			userData += pageTitle
		else:
			userData+="None"    

		tweetcnt += 1
		print 'Tweet:', tweetcnt, ' F.size = ', f.tell(), ' on file:', filecnt 
		userData += "\n"
		print userData
		f.write(userData)
		return True

	def on_error(self, status):
		print status
		if (status == 420):
			print "FOUND 420!!!"
			return False


if __name__ == '__main__':

	wait_counter = 0
	while crawlerFlag != False:
		try:
            #Authentication and connection to twitter API
			get_verificationAndRun()

			
		except Exception, e:
			print "Exception occured: "
			print e
			pass
	f.close()
