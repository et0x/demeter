'''
@author:		Michael Scott
@license:		GNU General Public License 2.0+
@contact:		et0x@rwnin.net
@organization:	rwnin.net
@desc:			Given a directory with *.pcap files in it, split each packet
						within each pcap file into it's own, separate pcap file.  Good
						for checking code coverage on single-packet pcaps ...
						usage: capsplit <directory_containing_pcaps>
'''

import struct
import sys
import os

def u(data):
	try:
		return struct.unpack("<I",data)
	except:
		return struct.unpack("<H",data)

def p(data):
	return struct.pack("<I",data).encode("hex")



class Pcap:

	def __init__(self,pcapFile):

		self.data 	= open(pcapFile,"rb").read(24)
		self.magic	= self.data[0:4]								# magic num
		self.majver	= u(self.data[4:6])							# major version number
		self.minver = u(self.data[6:8])							# minor version number
		self.tz			= u(self.data[8:12])						# GMT to local correction
		self.acc		= u(self.data[12:16])						# accuracy of timestamps
		self.snaplen= u(self.data[16:20])						# max len of captured packets
		self.net		= u(self.data[20:24])						# data link type
		self.hlen		= 24														# length of libpcap header
		self.header	= self.data											# raw global header data

class Packet:

	def __init__(self,pcapFile,offset=24):

		self.offset		= offset															# offset to this packet in pcap
		f 						= open(pcapFile,"rb")
		f.seek(self.offset)
		self.data			= f.read(16)
		f.close()
		self.pcapFile = pcapFile 														# path to pcap
		self.ts_sec		= u(self.data[:4])[0]									# timestamp seconds
		self.ts_usec	= u(self.data[4:8])[0]								# timestamp microseconds
		self.incl_len	= u(self.data[8:12])[0]								# num of actual bytes saved
		self.orig_len	= u(self.data[12:16])[0]							# length of packet when captured
		self.next			= self.offset + 16 + self.orig_len		# offset of the next packet
		self.plen			= self.orig_len + 16									# length of packet (incl header)
		f 						= open(pcapFile,"rb")
		f.seek(self.offset)
		self.packet   = f.read(self.plen)										# raw packet data (incl header)
		f.close()

	def _islast(self):	# last packet in the pcap ?
		
		if ((self.offset + self.plen + 1) > os.path.getsize(self.pcapFile)):
			return True
		else:
			return False

def usage():
	sys.stderr.write("[!] Usage: %s <directory_containing_pcaps>\n"%sys.argv[0])
	exit(-1)

def print_err(msg):
	sys.stderr.write("[!] Error: %s\n"%msg)

if len(sys.argv) != 2:
	usage()

if not os.path.exists(sys.argv[1]):
	print_err("Path doesn't exist!")
	exit(-1)

directory = sys.argv[1]

for _file in os.listdir(directory):
	if _file.endswith(".pcap"):
		f 		= os.path.join(directory,_file)
		fname	= _file.lower().replace(".pcap","")
		pcap 	= Pcap(f)
		packet 	= Packet(f)

		i = 1
		while True:
			if not packet._islast():
				open(os.path.join(directory,fname+"_"+str(i)+".pcap"),"wb").write(pcap.header+packet.packet)
				packet = Packet(f, packet.offset + packet.plen)
				i += 1
			else:
				open(os.path.join(directory,fname+"_"+str(i)+".pcap"),"wb").write(pcap.header+packet.packet)
				print "[*] PCAP '%s' processed, split into %d pcaps"%(fname,i)
				break