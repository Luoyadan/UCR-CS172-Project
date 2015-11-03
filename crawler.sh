#!/bin/sh

if [ -z "$2" ]; then
mkdir -p data
FILEPATH="data"
else
mkdir -p $2
FILEPATH=$2
fi

echo "Writing twitter data to /$FILEPATH ..." 
python twitterGeo.py $1 $FILEPATH 
