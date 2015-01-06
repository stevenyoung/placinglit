"""
handlers.export
"""
# pylint: disable=C0103

import ast
import json
import logging

from datetime import datetime

from google.appengine.api import users
from google.appengine.ext import db
# from google.appengine.ext import ndb
from google.appengine.ext import webapp

from handlers.abstracts import baseapp
from classes import placedlit
from classes import collections
from classes import site_users


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
      if place.book_data:
        loc['isbn13'] = place.book_data.isbn13
      if place.user_email:
        loc['user_email'] = place.user_email
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
    location = ast.literal_eval(self.request.get('location'))
    place = placedlit.PlacedLit(id=self.request.get('db_key'))
    place.location = db.GeoPt('{},{}'.format(location['latitude'],
                                             location['longitude']))
    place.timestamp = self.request.get('ts')
    if self.request.get('user_email'):
      place.user_email = self.request.get('user_email')
    else:
      place.user_email = 'info@placingliterature.com'
    place.google_user = users.User(place.user_email)
    scene_image = self.request.get('image_url')
    if scene_image != str('None'):  # ???
       place.image_url = scene_image
    place.ts = datetime.strptime(self.request.get('ts'), '%Y-%m-%d %X.%f')
    fields = ['actors', 'author', 'notes', 'scenedescription', 'scenelocation',
              'title', 'ug_isbn']
    for field in fields:
      setattr(place, field, self.request.get(field))
    place.put()


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


class SiteUserJSONExportHandler(baseapp.BaseAppHandler):
  """ export site user added and visited scenes """
  def get(self):
    export_users = site_users.User.query()
    user_list = list()
    for user in export_users.iter():
      logging.info('user:%s', user)
      user_data = dict()
      user_data['email'] = user.email
      scene_list = list()
      for scene_key in user.added_scenes:
        scene_data = dict()
        logging.info('scene key %s', scene_key)
        scene = db.get(scene_key.to_old_key())
        logging.info('%s:%s:%s', scene.title, scene.author, scene_key.id())
        scene_data['title'] = scene.title
        scene_data['author'] = scene.author
        scene_data['id'] = scene_key.id()
        scene_list.append(scene_data)
      user_data['added'] = scene_list
      user_list.append(user_data)
    self.response.out.write(json.dumps(user_list))

urls = [
  ('/places/dump', GetAllPlacesHandler),
  ('/places/import', ImportPlacesHandler),
  ('/places/csv_import/(.*)', CSVImportPlacesHandler),
  ('/places/missing_books', MissingBookSceneHandler),
  ('/users/scenes', SiteUserJSONExportHandler)
]


app = webapp.WSGIApplication(urls, debug="True")
