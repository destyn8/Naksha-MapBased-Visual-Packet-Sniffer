from scapy.all import sniff,get_if_addr,conf
from scapy.layers.inet import IP,ICMP,UDP, TCP
from socketIO_client import SocketIO
import time,requests,maxminddb
def getPublicIP(): 
	try: 
		response = requests.get('https://api.ipify.org') 
		if response.status_code == 200: 
			responseLoc = reader.get(str(response.text))
			responseCoords = [responseLoc['location']['latitude'],responseLoc['location']['longitude']]
			print(responseCoords)
			return responseCoords
		else: 
			return "Error: Unable to retrieve public IP address" 
	except Exception as e: 
		return f"Error: {e}" 
def retrieveCoords(srcIP,dstIP):
	location = None
	if srcIP == interProt or srcIP == gateWay:
		srcCoords = publicIP
		dstResponse = reader.get(dstIP)
		try:
			dstCoords = [(dstResponse['location']['latitude']),(dstResponse['location']['longitude'])]	
			location = [srcCoords,dstCoords]
		except:
			location = None
	elif dstIP == interProt or dstIP == gateWay:
		dstCoords = publicIP
		srcResponse = reader.get(srcIP)
		try:
			srcCoords = [(srcResponse['location']['latitude']),(srcResponse['location']['longitude'])]	
			location = [srcCoords,dstCoords]
		except:
			location = None
	print("location: ",location)
	return location
def extractIP(packet):
	if IP in packet:
		srcIP = packet[IP].src
		dstIP = packet[IP].dst
		if not(srcIP == interProt and dstIP == gateWay ) and not(srcIP == gateWay and dstIP == interProt):
			location = retrieveCoords(srcIP,dstIP)
			if location!=None:
				protocol = packet[IP].proto
				timeToLive = packet[IP].ttl
				packetLen = len(packet)
				sendServ('interProt',[srcIP,dstIP])
				sendServ('packetLen',packetLen)			
				sendServ('packetProt',protocol)			
				sendServ('packetTTL',timeToLive)			
				sendServ('newPacket',location)
				# time.sleep(5)
			else:
				print("nullHead")
def sendServ(packetDesc,location):
	sockIO.emit(packetDesc,location)
interProt = get_if_addr("wlp4s0")
gateWay = conf.route.route("0.0.0.0")[2]
reader = maxminddb.open_database('main-db-lookup.mmdb')
publicIP = getPublicIP()
sockIO = SocketIO('localhost',5000)
sendServ('packetHome',publicIP)
sniff(prn=extractIP,store=0)