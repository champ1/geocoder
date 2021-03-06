# -*- coding: utf-8 -*-

try:
	import requests
except:
	print 'Need to install Requests Module'
	
import sys


class Geocoder(object):
	def __init__(self, provider):
		self.provider = provider
		self.name = provider.name

		# Functions
		self.connect()
		self.add_data()

	def __repr__(self):
		return '<[{status}] Geocoder {name} [{address}]>'.format(status=self.status, name=self.name, address=self.address)

	def connect(self):
		""" Requests the Geocoder's URL with the Address as the query """
		try:
			r = requests.get(self.provider.url, params=self.provider.params, proxies=self.provider.proxies, timeout=5.0)
			self.url = r.url
			self.status = r.status_code
		except KeyboardInterrupt:
			sys.exit()
		except:
			self.status = 'ERROR - URL Connection'

		if self.status == 200:
			self.provider.load(r.json())
			self.json = self.provider.json

	def add_data(self):
		# Get Attributes
		self.status = self.provider.status()
		self.quality = self.provider.quality()
		self.location = self.provider.location
		self.x = self.provider.lng()
		self.y = self.provider.lat()
		self.ok = self.provider.ok()
		self.bbox = self.provider.bbox()
		self.address = self.provider.address()
		self.postal = self.provider.postal()
		self.quality = self.provider.quality()

		# More ways to spell X.Y
		x, y = self.x, self.y
		self.lng, self.longitude = x, x
		self.lat, self.latitude = y, y
		self.latlng = '{0}, {1}'.format(self.lat, self.lng)
		self.xy = '{0}, {1}'.format(x, y)

		# Bounding Box - SouthWest, NorthEast - [y1, x1, y2, x2]
		self.south = self.provider.south
		self.west = self.provider.west
		self.southwest = '{0}, {1}'.format(self.south, self.west)
		self.north = self.provider.north
		self.east = self.provider.east
		self.northeast = '{0}, {1}'.format(self.north, self.east)

		# Build JSON
		self.json = self.build_json()

	def build_json(self):
		json = dict()
		json['provider'] = self.name
		json['location'] = self.location
		json['ok'] = self.ok
		json['status'] = self.status
		
		if self.ok:
			json['quality'] = self.quality

		if self.postal:
			json['postal'] = self.postal

		if self.address:
			json['address'] = self.address

		if self.ok:
			json['x'] = self.x
			json['y'] = self.y
			json['latlng'] = self.latlng
			json['xy'] = self.xy

		if self.east:
			json['bbox'] = self.bbox
			json['east'] = self.east
			json['west'] = self.west
			json['north'] = self.north
			json['south'] = self.south
			json['northeast'] = self.northeast
			json['southwest'] = self.southwest

		return json

	def debug(self):
		print '============'
		print 'Debug Geocoder'
		print '-------------'
		print 'Provider:', self.name
		print 'Address:', self.address
		print 'Location:', self.location
		print 'LatLng:', self.latlng
		print 'Bbox:', self.bbox
		print 'South-West:', self.southwest
		print 'North-East:', self.northeast
		print 'OK:', self.ok
		print 'Status:', self.status
		print 'Quality:', self.quality
		print 'Postal:', self.postal
		print 'Url:', self.url
		print '============'
		print 'JSON Objects'
		print '------------'
		for item in self.provider.json.items():
			print item

if __name__ == '__main__':
	"""
	Providers
	=========
	Google
	Bing
	TomTom
	Mapquest
	Nokia
	Esri
	OSM
	Maxmind
	"""

	from google import Google

	location = 'Ottawa Ontario'
	proxy = {'http':'http://124.42.13.230:8080'}
	g = Geocoder(Google(location, proxies=proxy))
	print g.debug()

