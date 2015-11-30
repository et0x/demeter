'''
@author:		Michael Scott
@license:		GNU General Public License 2.0+
@contact:		et0x@rwnin.net
@organization:	rwnin.net
'''
from bs4 import BeautifulSoup
from collections import OrderedDict

import urllib
import json
import time
import pprint

# demeter imports
#import formats

class google_searcher:
	'''
	Searcher responsible for interacting with google search results
	'''
	def __init__(self, apikey, searchEngineID):
		self.searchEngineID = searchEngineID
		self.apikey 		= apikey
		self.engine 		= "google"

	def _build_url(self, query, startnum):
		search_parameters = OrderedDict([
			('cx', 	self.searchEngineID),
			('key',	self.apikey),
			('rsz', 10),
			('num', 10),
			('googlehost', 'www.google.com'),
			('gss', '.com'),
			('q', query),
			('oq', query),
			('filter', 0),
			('safe', 'off'),
			('start', startnum)
			])
		return 'https://www.googleapis.com/customsearch/v1?{}'.format(urllib.urlencode(search_parameters))

	def _verify_file(self,url,ext):
		pass

	def search(self, filetypes,numresults):
		self.filetypes 	= filetypes
		resultCount 	= 0
		currentResult 	= 0
		totalresults = 0
		urls = []

		for ext in filetypes:
			while (totalresults < numresults):
				searchurl = self._build_url("filetype:%s"%ext, totalresults)
				response = urllib.urlopen(searchurl).read()
				response = json.loads(response)
				try:
					results = response["items"]
				except KeyError:
					break
				for result in results:
					urls.append(result["link"])
					totalresults += 1
				time.sleep(1)
		return urls