import json
import logging

from google.appengine.ext import webapp
from google.appengine.ext import users

from handlers.abstracts import baseapp

from classes import collections
from classes import placedlit


class SceneCollectionHandler(baseapp.BaseAppHandler):
  """ Web handler for scene collections """
  def get(self, collection_name):
    scene_keys = collections.Collection().get_named(collection_name)
    scene_json = dict()
    for key in scene_keys:
      place = placedlit.PlacedLit().get_by_key_name(key)
      logging.info('place:', key, place)
      scene_json.append({'title': place.title})

urls = [('/collections/(.*)', SceneCollectionHandler)]

app = webapp.WSGIApplication(urls, debug=True)
