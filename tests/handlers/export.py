"""
handlers.export
"""

import ast
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

from handlers.abstracts import baseapp
from classes import placedlit


class GetAllPlacesHandler(baseapp.BaseAppHandler):
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
        'author': place.author,
        'scenedescription': place.scenedescription,
        'notes': place.notes,
        # 'ts': place.ts,
        'location': location_export,
        'checkins': place.checkins,
        'image_url': place.image_url,
        'db_key': key.id()}
      loc_json.append(loc)
    self.output_json(loc_json)


class ImportPlacesHandler(baseapp.BaseAppHandler):
  def post(self):

    place = placedlit.PlacedLit(
      actors=self.request.get('actors'),
      author=self.request.get('author'),
      checkins=int(self.request.get('checkins')),

      notes=self.request.get('notes'),
      scenedescription=self.request.get('scenedescription'),
      scenelocation=self.request.get('scenelocation'),
      scenetime=self.request.get('scenetime'),
      symbols=self.request.get('symbols'),
      title=self.request.get('title')
    )
    # image_url=ast.literal_eval(self.request.get('image_url'))
    # if image_url:
    #   logging.info('image url:{}'.format(self.request.get('image_url')))
    #   place.image_url = self.request.get('image_url')
    location = ast.literal_eval(self.request.get('location'))
    place.location = db.GeoPt(
      lat=location['latitude'],
      lon=location['longitude']
    )
    place.put()

urls = [
  ('/places/dump', GetAllPlacesHandler),
  ('/places/import', ImportPlacesHandler)
]


app = webapp.WSGIApplication(urls, debug="True")
