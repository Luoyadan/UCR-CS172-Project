#!/bin/sh

if [ -z "$2" ]; then
FILEPATH=$1
TWEETS=0
mkdir -p $1
elif [ -z "$1" ]; then
TWEETS=0
mkdir -p data
FILEPATH="data"
else
TWEETS=$1
DATAPATH=$2
mkdir -p $2
fi

echo "Writing twitter data to /$FILEPATH ..." 
python twitterGeo.py $TWEETS $FILEPATH 
