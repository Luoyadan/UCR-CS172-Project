Python Twitter Crawler
====

Licensing Information: MIT
---
Project source can be downloaded from https://github.com/khuan013/CS172-Crawler.git

Author & Contributor List
----
* Kenneth Huang
* Tien Tran


Overview
-------

Part 1 Crawler

This application uses the Twitter Streaming API to collect geolocated tweets and stores them in text files of 10MB each.

Instructions on how to deploy the system
-------

In order to run the program, you must have: 

* Python 2.7
* Tweepy Twitter API library installed.
* lxml 

Download the repository from https://github.com/khuan013/CS172-Crawler.git

If on Unix/Linux, run the crawler.sh shellscript, and pass the number of tweets you want to search (if the number is 0, the crawler will go on untill it reaches 5 GB in data) and output directory name, which will execute the Python program. 

By default, the files are placed in /data and number of tweets are not limited. 

Examples:

1. ./crawler.sh [num-tweets] [output-dir] 
2. ./crawler.sh [num-tweets]
3. ./crawler.sh 

Part 2 Indexing/Webpage

Instructions on how to deploy the system
-------

In order to run the program you must have the following installed:
* Eclipse for Java EE
* Apache Tomcat version 7.0
* Lucene version 3.7.2

1. Download the repository from https://github.com/khuan013/CS172-Crawler.git
2. Put MyLucene.java and MySearch.jsp into your Eclipse project directory. 
3. If you already have twitter data, run MyLucene.java to create an index. Otherwise run the python program twitterGeo.py, refer to Part A documentation on how to use it. 
4. Once MyLucene.java finishes it will create a folder called testIndex. Put this folder at your Desktop directory. 
5. Run MySearch.jsp on the tomcat servers using Eclipse. This should bring up a webpage with a search bar. 
