from scapy.all import sniff,get_if_addr,conf
from scapy.layers.inet import IP
from socketIO_client import SocketIO
import time,requests
def getPublicIP(): 
	try: 
		response = requests.get('https://api.ipify.org') 
		if response.status_code == 200: 
			responseLoc = requests.get(f"https://geolocation-db.com/json/{str(response.text)}&position=true").json()
			responseCoords = [responseLoc['latitude'],responseLoc['longitude']]
			return responseCoords
		else: 
			return "Error: Unable to retrieve public IP address" 
	except Exception as e: 
		return f"Error: {e}" 
def retrieveCoords(srcIP,dstIP):
	if srcIP == interProt or srcIP == gateWay:
		srcCoords = publicIP
		dstResponse = requests.get(f"https://geolocation-db.com/json/{str(dstIP)}&position=true").json()
		dstCoords = [dstResponse['latitude'],dstResponse['longitude']]	
		location = [srcCoords,dstCoords]
	elif dstIP == interProt or dstIP == gateWay:
		dstCoords = publicIP
		srcResponse = requests.get(f"https://geolocation-db.com/json/{str(srcIP)}&position=true").json()
		srcCoords = [srcResponse['latitude'],srcResponse['longitude']]	
		location = [srcCoords,dstCoords]
	return location
def extractIP(packet):
	if IP in packet:
		srcIP = packet[IP].src
		dstIP = packet[IP].dst
		if not(srcIP == interProt and dstIP == gateWay ) and not(srcIP == gateWay and dstIP == interProt):
			location = retrieveCoords(srcIP,dstIP)
			sendServ(location)
def sendServ(location):
	sockIO.emit('newPacket',location)
	print("location sent")
interProt = get_if_addr("wlp4s0")
gateWay = conf.route.route("0.0.0.0")[2]
publicIP = getPublicIP()
sockIO = SocketIO('localhost',5000)
sniff(prn=extractIP,store=0)