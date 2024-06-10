from scapy.all import sniff,get_if_addr,conf
from scapy.layers.inet import IP
import time,requests
def extractIp(packet):
	ip = get_if_addr("wlp4s0")
	gw = conf.route.route("0.0.0.0")[2]
	if IP in packet :
		src = packet[IP].src
		dst = packet[IP].dst
		if not(src == ip and dst == gw ) and not(src == gw and dst == ip):
			src_response = requests.get(f"https://geolocation-db.com/json/{str(src)}&position=true").json()
			dst_response = requests.get(f"https://geolocation-db.com/json/{str(dst)}&position=true").json()
			src_coords = [src_response['latitude'],src_response['longitude']]
			dst_coords = [dst_response['latitude'],dst_response['longitude']]
			print(f"Source:{src_coords} | {src}\nDestination:{dst_coords} | {dst}\n\n")
while True:
	sniff(prn=extractIp, count=10)
	time.sleep(5)
# latitude = response['latitude']
# longitude = response['longitude']
# print(latitude,longitude)
# gw = scapy.conf.route.route("0.0.0.0")[2]
# interfaces = scapy.get_if_list()
