#!/bin/bash

_BASE_URL='http://example.com/audio-books'
_DIR=ASoIaF2_CoK
_BOOK_NAME="A Clash of Kings"
_BOOK_ORDER="second"
_BOOK_DESC="$_BOOK_NAME, the $_BOOK_ORDER book of the A Song of Ice and Fire series by George R. R. Martin" 
_FILE_SEED_DATE="1998-11-16 06:30 PST"

#Download the podcastgen script
curl -L --silent https://gist.githubusercontent.com/alghanmi/11102772/raw/podcastgen.py > podcastgen.py 

#Changes the file dates to make them in ascending order. This is a hack to make it work
#  with Podcatchers that rely on date for order
if [ -n "$_FILE_SEED_DATE" ]; then
        SAVEIFS=$IFS
        IFS=$(echo -en "\n\b")

        _cnt=0
        for i in $(find $_DIR -type f | sort); do
                (( _cnt += 1 ))
                _file_date="$(date -d "$_FILE_SEED_DATE + $_cnt days" +'%Y%m%d%H%M')"
                touch -t $_file_date $i
        done
        IFS=$SAVEIFS

fi

#Generate Podcast for requested file
python podcastgen.py gen $_DIR \
   --title       "$_BOOK_NAME" \
   --desc        "$_BOOK_DESC" \
   --link        "$_BASE_URL/$_DIR"             \
   --id          "$_BASE_URL/$_DIR"             \
   --feed-link   "$_BASE_URL/$_DIR/podcast.xml" \
   --logo        "$_BASE_URL/$_DIR/logo.jpg"    \
   --category    "Arts" \
   --subcategory "Literature" \
   --language    "en" \
   --output      podcast_$DIR.xml

#Pretty print the podcast XML file
cat podcast_$DIR.xml | xmllint --format - > $_DIR/podcast.xml && rm podcast_$DIR.xml
