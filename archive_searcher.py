import urllib
import json
import sys
import pprint
import string

class archive_searcher:
	def __init__(self,maxResults):
		self.maxResults		= maxResults
		self.urlAvailable	= "https://archive.org/advancedsearch.php?q=%s&mediatype=&rows=1&page=1&output=json&save=no#raw"
		self.urlGetTitles	= "https://archive.org/advancedsearch.php?q=%s&mediatype=&rows=%d&page=1&output=json&save=no#raw"
		self.urlGetURL		= "https://archive.org/details/%s&output=json&callback=IAE.favorite"
		self.engine			= "archive"

	def _find_available(self,extension):
		'''
		Searcher._find_available("exe")
		returns number of files of given type
		available for download
		'''
		self.extension		= extension
		self.numberFound	= json.loads(
			urllib.urlopen(self.urlAvailable%self.extension).read()
			)["response"]["numFound"]
		return self.numberFound

	def _get_titles(self):
		'''
		Searcher._get_titles()
		returns a list of titles for files which
		is required for final query to download file
		'''
		queryNum			= min(self.maxResults,self.numberFound)			# only return the max results we want
		data				= json.loads(
			urllib.urlopen(self.urlGetTitles%(self.extension,queryNum)).read()
			)

		results = []
		for i in xrange(self.numberFound -1):
			try:
				# to prevent multiple lookups:
				d = data["response"]["docs"][i]["title"]

				# file ends with correct extension?
				if d.lower().endswith(".%s"%self.extension.lower()):

					# all characters in filename printable?
					if all(c in string.printable for c in d):

						# replace spaces with underscores
						if " " in d:
							results.append(d.replace(" ","_"))
						else:
							results.append(d)
			except:
				pass

			# stop collecting filenames if we hit max result threshold
			if (len(results) == (self.maxResults)):
				return results
		return results

	def _get_urls(self,filenames):
		'''
		Searcher._get_urls(fileNameList[])
		returns a list of links to download files,
		given a list of filenames from the 
		_get_titles method
		'''
		results = []
		for filename in filenames:
			try:
				data = json.loads(
					# json response is encapsulated by IAE.favorite( ... ), hence the [13:-1] crop
					urllib.urlopen(self.urlGetURL % filename).read()[13:-1]
					)
				link = "https://%s%s/%s"%( data["server"], data["dir"],data["dir"].split("/")[-1])
				results.append(link)
			except:
				pass
		return results

