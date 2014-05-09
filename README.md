#Podcast Feed Generator
Generate an podcast RSS feed for a set of media in a directory.

`podcastgen` is a wrapper for the [feedgen](http://lkiesow.github.io/python-feedgen/) python module.

##Usage instructions
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

##Use Case -- AudioBooks from Library
A good number of public libraries contract with [OverDrive](https://www.overdrive.com/) to provide digital media to its patrons. Their collection include Audiobooks. Unfortunately, they only have Windows and Mac clients, however, you can use [wine](http://www.winehq.org/) to run their Windows client:
```bash
#install required packages
aptitude install wine winetricks

#install Windows Media Player 10
winetricks wmp10

#Install OverDrive MediaConsole
wine msiexec /i ODMediaConsoleSetup.msi
```

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
  + Some podcatchers are sensitive to the date timestamps of the file. [Here is an example](https://github.com/alghanmi/PodcastFeedGenerator/blob/master/sample_gen.sh#L13-L27) of how you can fix that.
