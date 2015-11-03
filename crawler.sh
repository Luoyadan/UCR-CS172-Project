#!/bin/sh

if [ -z "$1" ]; then
mkdir -p data
FILEPATH="data"
else
mkdir -p $1
FILEPATH=$1
fi

echo "Writing twitter data to /$FILEPATH ..." 
python twitterGeo.py $FILEPATH $2
