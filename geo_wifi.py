#!/usr/bin/env python
# -*- coding: utf-8 -*-

# seach geo location from wifi mac address
# 2016-06-20 K.OHWADA

from selenium import webdriver
import sys
import urllib
import urllib2
import json
import time

KEY = "your_key"
CMD_CHROMEDRIVER = "/usr/local/bin/chromedriver"

#
# GeoWifi
#
class GeoWifi():

	HEADERS = { 'Content-Type' : 'application/json' }

	def request(self, key, addr1, addr2 ):
		url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + key
		text = self.buildJson( addr1, addr2 )
#		print text
		req = urllib2.Request(url, text, self.HEADERS)
		res = urllib2.urlopen(req)
		body = res.read()
#		print body
		return self.parseResponse(body)

	def buildJson(self, addr1, addr2):
		obj = {}
		obj[ "wifiAccessPoints" ] = self.buildAddressList(addr1, addr2)
		text = json.dumps(obj)
		return text
	
	def buildAddressList(self, addr1, addr2):
		list = []
		list.append( self.buildAddress(addr1) )
		list.append( self.buildAddress(addr2) )
		return list

	def buildAddress(self, addr):
		dict = { "macAddress": addr }
		return dict

	def parseResponse(self, res):
		obj = json.loads(res)
		if obj["location"] is None:        
			print res
			return None
		if obj["location"]["lat"] is None:   
			print res
			return None
		if obj["location"]["lng"] is None:   
			print res
			return None
		if obj["accuracy"] is None: 
			accuracy = 0  
		else:
			accuracy = obj["accuracy"]  	
		ret = {}	
		ret["lat"] = obj["location"]["lat"]
		ret["lng"] = obj["location"]["lng"]		
		ret["accuracy"] = accuracy	
		return ret

# class end

def openChrome(lat, lng):
	url = "https://maps.google.co.jp/maps?q=" + str(lat) + "," + str(lng) + "&z=12"
	driver = webdriver.Chrome( CMD_CHROMEDRIVER )
	driver.get(url);

# main
args = sys.argv
argc = len(args)
if (len(args) < 3):
	print 'Usage: python %s mac_addr_1 mac_addr_2' % args[0]
	exit()

geo = GeoWifi()
res = geo.request( KEY, args[1], args[2] )
if res is None:
	exit()

print str(res["lat"]) + " " + str(res["lng"]) + " "+ str(res["accuracy"])
openChrome( res["lat"], res["lng"] )

print "Press CTRL+C to quit"
try:
	# endless loop
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	# exit the loop, if key interrupt
	pass

# end		