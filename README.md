##Podcast Feed Generator
Generate an podcast RSS feed for a set of media in a directory.

`podcastgen` is a wrapper for the [feedgen](http://lkiesow.github.io/python-feedgen/) python module.

###Usage instructions
For usage instructions including arguments and options, run the following command:
```bash
python podcastgen.py --help
```

###Dependencies:
  + [docopt](http://docopt.org/) &mdash; a Command-line interface description language
```
pip install docopt
```

  + [feedgen](http://lkiesow.github.io/python-feedgen/) &mdash; a Python module to generate ATOM feeds, RSS feeds and Podcasts
```
pip install feedgen
```

  + [mutagen]() &mdash; a Python module to handle audio metadata
```
pip install mutagen
```

###Example
[sample generator](sample_gen.sh) script shows how to create a podcast feed for one of the Game of Thrones books. The basic command looks like:
```bash
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
```

###Notes
  + Some podcatchers are sensitive to the date timestamps of the file. Here is an example of how you can fix that.
