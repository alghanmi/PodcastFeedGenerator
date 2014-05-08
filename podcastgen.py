"""Podcast Feed Generator
 
Generate an podcast RSS feed for a set of media in a directory.
Use the list-extensions argument to see the list of supported extensions. You can add custom extensions using
 
Usage:
	podcastgen.py gen <directory> --title=<podcast-title> --link=<podcast-link> --desc=<description> [--output=<rss-feed-file>] [--feed-link=<feed-url>] [--id=<podcast-id>] [--logo=<image_file>] [--category=<itunes-category> [--subcategory=<itunes-category>]] [--language=<language>] [--use-extension=<ext>]
	podcastgen.py list-categories
	podcastgen.py list-extensions
	podcastgen.py -h | --help
	podcastgen.py --version
 
Arguments:
	gen					Generate the podcast
	list-categories		Show all Podcast categories
	list-extensions		List all supported extensions
	<directory>			the directory containing all the files
 
Options:
	--title				The title of the podcast
	--link				URL associated with the podcast (i.e. podcast webpage)
	--desc				A short description of the podcast
	--id				Feed id is a universally unique URI
	--feed-link			URL for the Podcast feed itself
	--logo				Logo file for the feed
	--category			iTunes category for podcast
	--subcategory		iTunes sub-category based on the iTunes list above
	--language			The language of the podcast using the two-character language id, e.g. en, fr or de
	--use-extension		Add an extension to the list of supported extensions when generating the podcast
	--output			Write-output to <rss-feed-file>. Default is 
	-h --help			Show this screen
	--version			Show version

Dependencies:
	docopt  - pip install docopt
	feedgen - pip install feedgen
	mutagen - pip install mutagen
"""

from docopt import docopt
import datetime
from feedgen.entry import FeedEntry
from feedgen.ext import podcast
from feedgen.ext import podcast_entry
from feedgen.ext.podcast import PodcastExtension
from feedgen.feed import FeedGenerator
import mimetypes
import mutagen
from mutagen.easyid3 import EasyID3
import os
import re
import urllib

_podcast_file_extensions = [ 'avi', 'm4a', 'm4v', 'mov', 'mp3', 'mp4', 'ogg', 'wav', 'wmv', 'flac' ]


def get_media_file_pattern(extra_extensions=None):
	''' Generate the Regular Expression to match all podcast files '''
	pattern = ''
	if extra_extensions is not None:
		_podcast_file_extensions.append(extra_extensions)
	
	for ext in _podcast_file_extensions:
		pattern = '{}|.*\.{}'.format(pattern, ext)
	
	return pattern[1:]

def check_category(category, subcategory=None):
	''' Check the validity of a provided category '''
	if category in PodcastExtension._itunes_categories and subcategory is None:
		return True
	elif category in PodcastExtension._itunes_categories is not None and subcategory in PodcastExtension._itunes_categories[category] is not None:
		return True
	
	return False

def get_feed_entry(media_file, basedir, baselink, image_url):
		''' Generate a feed entry based on ID3 Data
			TODO: Deal with files with no ID3 Data
		'''
		fe = FeedEntry ()
		fe.load_extension('podcast')
		
		file_path = '{}/{}'.format(basedir, media_file)
		media_info = EasyID3(file_path)
		media_length_s = mutagen.File(file_path).info.length
		media_length = datetime.timedelta(seconds=round(media_length_s))
		
		fe.title(media_info['title'][0])
		fe.description('Part {} of {}'.format(media_info['tracknumber'][0], media_info['album'][0]))
		fe.podcast.itunes_duration(media_length)
		
		url = '{}/{}'.format(baselink, urllib.pathname2url(media_file))
		fe.id(url)
		fe.link(href=url, rel='alternate')
		fe.pubdate('{} +0000'.format(datetime.datetime.utcfromtimestamp(os.path.getmtime(file_path))))
		fe.enclosure(url, str(os.path.getsize(file_path)), mimetypes.guess_type(file_path)[0])
		#Found no need to for this at this time since all podcasts have the same feed image
		#fe.podcast.itunes_image(image_url)
		
		return fe

if __name__ == '__main__':
	args = docopt(__doc__, version='PodcastGen v0.6')
	#pprint(args)
	
	''' Generate Podcast Feed '''
	if args['gen'] is True:
		#Check if <directory> exists and readable
		if os.path.exists(args['<directory>']) is False:
			print '[ERROR] Directory "{}" does not exist'.format(args['<directory>'])
			exit(1)
		elif os.path.isdir(args['<directory>']) is False:
			print '[ERROR] "{}" does represent a directory'.format(args['<directory>'])
			exit(1)
		
		#Get File list and prune out all non-podcast files
		feed_files = []
		media_re = re.compile(get_media_file_pattern(args['--use-extension']), re.IGNORECASE)
		for root, dirs, all_files in os.walk(args['<directory>']):
			for f in all_files:
				if media_re.match(f) is not None:
					feed_files.append(f)
		feed_files.sort()	
		
		#Exit program if no files match
		if len(feed_files) <= 0:
			print '[ERROR] "{}" does not have any podcast media files'.format(args['<directory>'])
			exit(1)
			
		
		#Initialize Podcast feed
		fg = FeedGenerator()
		fg.load_extension('podcast')
		
		#Check if [sub]categories are valid
		if(args['--category'] is not None):
			if check_category(args['--category'], args['--subcategory']) is False:
				print '[ERROR] Invalid podcast categories. Use the the list-categories option to see valid categories'
				exit(1)
			if args['--subcategory'] is not None:
				fg.podcast.itunes_category(args['--category'], args['--subcategory'])
			else:
				fg.podcast.itunes_category(args['--category'])
		
		#Podcast Details
		fg.title(args['--title'])
		fg.link(href=args['--link'], rel='alternate')
		fg.description(args['--desc'])
		
		if args['--id'] is not None:
			fg.id(args['--id'])
		
		if args['--logo'] is not None:
			fg.logo(logo=args['--logo'])
			fg.image(url=args['--logo'], title=args['--title'])
			fg.podcast.itunes_image(args['--logo'])
			
		if args['--language'] is not None:
			fg.language(args['--language'])
			
		if args['--feed-link'] is not None:
			fg.link(href=args['--feed-link'], rel='self')
		
		#Clean-up link string: trim spaces and remove trailing slash
		link = args['--link'].strip()
		if link[len(link) - 1] == '/':
			link = link[:len(link)-1]
		
		#Generate feed items from files in directory.
		for item in feed_files:
			fg.add_entry(get_feed_entry(item, args['<directory>'], link, args['--logo']))
	
		#Write RSS feed
		feed_file = 'podcast.xml'
		if args['--output'] is not None:
			feed_file = args['--output']
		fg.rss_str(pretty=True)
		fg.rss_file(feed_file)
	
	elif args['list-categories'] is True:
		for cat in PodcastExtension._itunes_categories:
			print '+ {}'.format(cat)
			for sub in PodcastExtension._itunes_categories[cat]:
				print'\t- {}'.format(sub)

	elif args['list-extensions'] is True:
		for ext in _podcast_file_extensions:
			print '{}'.format(ext)