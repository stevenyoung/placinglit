"""
handlers.export
"""
# pylint: disable=C0103

import ast
import json
import logging

from google.appengine.ext import webapp
from google.appengine.api import users

from handlers.abstracts import baseapp
from classes import placedlit
from classes import collections


class GetAllPlacesHandler(baseapp.BaseAppHandler):
  """ get all places as a json dump. useful for setting up dev environments """
  def get(self):
    places = placedlit.PlacedLit.get_all_places()
    loc_json = []
    for place in places:
      geo_pt = place.location
      location_export = {
        'latitude': geo_pt.lat,
        'longitude': geo_pt.lon
      }
      key = place.key()
      loc = {
        'title': place.title,
        'author': place.author,
        'scenelocation': place.scenelocation,
        'scenetime': place.scenetime,
        'actors': place.actors,
        'symbols': place.symbols,
        'scenedescription': place.scenedescription,
        'notes': place.notes,
        'location': location_export,
        'checkins': place.checkins,
        'image_url': place.image_url,
        'ts': place.ts.strftime('%Y-%m-%d %X.%f'),
        'db_key': key.id()}
      if place.ug_isbn:
        loc['ug_isbn'] = place.ug_isbn
      if place.user_email:
        loc['user_email'] = place.user_email
      logging.info('timestamp: %s', place.ts)
      loc_json.append(loc)
    self.output_json(loc_json)


class CSVImportPlacesHandler(baseapp.BaseAppHandler):
  """ import places from csv and add to a collection """
  def post(self, collection_name):
    collection = collections.Collection().create_or_update(collection_name)
    data = json.loads(self.request.body)
    data['email'] = collections.FEATURED[collection_name]['user']
    data['user'] = users.User(data['email'])
    if 'notes' not in data:
      data['notes'] = ''
    place_key = placedlit.PlacedLit.create_from_dict(data)
    collection.add_scene(place_key)


class ImportPlacesHandler(baseapp.BaseAppHandler):
  """ import scenes from json """
  def post(self):
    data = {'actors': self.request.get('actors'),
            'author': self.request.get('author'),
            'current_checkin_count': int(self.request.get('checkins')),
            'notes': self.request.get('notes'),
            'scene': self.request.get('scenedescription'),
            'place_name': self.request.get('scenelocation'),
            'title': self.request.get('title'),
            'email': self.request.get('user_email')
            }
    if not data['email']:
      data['email'] = 'info@placingliterature.com'
    data['user'] = users.User(data['email'])
    location = ast.literal_eval(self.request.get('location'))
    data['longitude'] = location['longitude']
    data['latitude'] = location['latitude']
    if self.request.get('ts'):
      data['timestamp'] = self.request.get('ts')
    placedlit.PlacedLit.create_from_dict(data)


class MissingBookSceneHandler(baseapp.BaseAppHandler):
  """ list scenes missing book data """
  def get(self):
    places = placedlit.PlacedLit.get_all_unresolved_places()
    place_json = []
    for place in places:
      geo_pt = place.location
      location_export = {
        'latitude': geo_pt.lat,
        'longitude': geo_pt.lon
      }
      key = place.key()
      loc = {
        'title': place.title,
        'author': place.author,
        'location': location_export,
        'checkins': place.checkins,
        'db_key': key.id()}

      if place.ug_isbn:
        loc['ug_isbn'] = place.ug_isbn
      else:
        loc['ug_isbn'] = ''

      place_json.append(loc)
    self.output_json(place_json)


urls = [
  ('/places/dump', GetAllPlacesHandler),
  ('/places/import', ImportPlacesHandler),
  ('/places/csv_import/(.*)', CSVImportPlacesHandler),
  ('/places/missing_books', MissingBookSceneHandler)
]


app = webapp.WSGIApplication(urls, debug="True")
