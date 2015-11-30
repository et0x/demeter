import threading
import Queue
import os
import urllib

class downloader(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self, name=os.urandom(16).encode("hex"))
		self.q = queue

	def run(self):
		while True:
			url = self.q.get()
			self.download(url)
			self.q.task_done()

	def download(self, url):
		req = urllib.open(url)
		if (req.getcode() == 200):
			print "[+] Successfully downloaded a file: %s"%url
		else:
			pass


class download_handler:
	def __init__(self, urlList, threadCount=10):
		self.threadCount 	= threadCount
		self.urlList		= urlList

	def _begin_downloading(self):
		q 	= Queue.Queue()

		for i in range(self.threadCount):
			t = downloader(q)
			t.setDaemon(True)
			t.start()

		for url in self.urlList:
			q.put(url)

		q.join()
		return