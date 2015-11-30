import ConfigParser
import archive_searcher
import google_searcher
import downloader
import sys
import os

class session:

	def __init__(self):
		self.__installdir__ = os.path.dirname(os.path.realpath(__file__))
		self.cfgParser 	= ConfigParser.SafeConfigParser()
		self.cfgFile	= "config.ini"
		__installdir__ = os.path.dirname(os.path.realpath(__file__))
		self.cfgParser.read(os.path.join(self.__installdir__,self.cfgFile))

		try:
			self.google_apikey 	= self.cfgParser.get("search_options","google_api_key")
		except:
			self.google_apikey 	= ""

		try:
			self.google_seid 	= self.cfgParser.get("search_options","google_se_id")
		except:
			self.google_seid 	= ""

		try:
			self.maxResults		= self.cfgParser.get("search_options","default_maxresults")
		except:
			self.maxResults		= 0

	def execute(self, extension, maxResults):
		self.extension 		= extension
		self.searcher 		= archive_searcher.archive_searcher(self.maxResults)
		self.numresults 	= self.searcher._find_available(self.extension)
		self.engine			= "archive"

		if self.numresults:
			sys.stderr.write("[*] Archive.org search completed, results: %d\n"%self.numresults)
		else:
			# archive.org didn't have filetype searched for, use google now
			if (self.google_apikey and self.google_seid):
				sys.stderr.write("[*]  Archive.org had no results, attempting with Google Custom Search API\n")
				self.searcher = google_searcher.google_searcher(self.google_apikey,self.google_seid)
			else:
				sys.stderr.write("[!]  Archive.org had no results, and you haven't specified Google Custom Search API Info ...\n")
				sys.stderr.write("[!]  If you wish to use Google Custom Search API as an alternate, edit 'config.ini'\n")

		if self.searcher.engine == "archive":
			sys.stderr.write("[*] Gathering filenames from Archive.org ...\n")
			self.filenames = self.searcher._get_titles()

		if self.searcher.engine == "archive":
			self.urls = self.searcher._get_urls(self.filenames)
			sys.stderr.write("[*] Archive.org search completed, gathered urls: %d\n"%len(self.urls))
		else:
			self.urls = self.searcher.search(self.extension,self.maxResults)
			sys.stderr.write("[*]  Google Custom Search API search completed, gathered urls: %d"%len(self.urls))


		# from this point, we have a list of urls of possible files to download
		# stored in self.urls ... Now we have to download the files and verify
		# the magic numbers of them in order to store them
		self.downloader = downloader.download_handler(self.urls)
		self.downloader._begin_downloading()