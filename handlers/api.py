""" api handler """
# pylint: disable=W0403, R0904, C0103


import json
import logging


from google.appengine.ext import webapp
from handlers.abstracts import baseapp

from classes import placedlit


class APIPlacesHandler(baseapp.BaseAppHandler):
  def get(self):  # retrieve all
    logging.info('API Places get all')
    places = placedlit.PlacedLit.get_all_places()
    # loc_json = []
    # for place in places:
    #   place_dict = {
    #     'latitude': place.location.lat,
    #     'longitude': place.location.lon,
    #     'db_key': place.key().id(),
    #     'title': place.title,
    #     'author': place.author
    #   }
    #   loc_json.append(place_dict)
    loc_json = [self.export_place_fields(place) for place in places]
    self.output_json(loc_json)

  def post(self):  # create new, return id
    json_data = json.loads(self.request.body)
    logging.info('API Places post %s', json_data)


class APIPlaceHandler(baseapp.BaseAppHandler):
  def get(self, id):  # retrieve by id
    logging.info('API Place get id: %s', id)

  def put(self, id):  # update resource by id
    logging.info('API Place put id: %s', id)

  def delete(self, id):  # delete resource by id
    logging.info('API Place delete id: %s', id)


urls = [
  ('/api/places', APIPlacesHandler),
  ('/api/places/(.*)', APIPlaceHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
