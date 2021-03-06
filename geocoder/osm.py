# -*- coding: utf-8 -*-

from base import Base


class Osm(Base):
    name = 'OSM'
    url = 'http://nominatim.openstreetmap.org/search'

    def __init__(self, location):
        self.location = location
        self.json = dict()
        self.params = dict()
        self.params['format'] = 'json'
        self.params['q'] = location

    def lat(self):
        return self.safe_coord('lat')
        
    def lng(self):
        return self.safe_coord('lon')

    def address(self):
        return self.safe_format('display_name')

    def quality(self):
        return self.safe_format('type')

    def postal(self):
        return self.safe_postal(self.address())

    def bbox(self):
        southwest = self.json.get('boundingbox-0'), self.json.get('boundingbox-2')
        northeast = self.json.get('boundingbox-1'), self.json.get('boundingbox-3')
        return self.safe_bbox(southwest, northeast)