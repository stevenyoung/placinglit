""" Handle web requests for collections """
# pylint disable=C0103
import json
import logging

from google.appengine.ext import db
from google.appengine.ext import deferred
from google.appengine.ext import webapp

from handlers.abstracts import baseapp

from classes import collections
from classes import placedlit

import update_schema


class SceneCollectionHandler(baseapp.BaseAppHandler):
  """ Web handler for scene collections """
  def get(self, collection_name):  # pylint disable=W0221
    """ get request for collection """
    template_values = self.basic_template_content()
    template_values['title'] = 'Map'
    scene_keys = collections.Collection().get_named(collection_name).scenes
    if 'center' in collections.FEATURED[collection_name]:
      collection_center = collections.FEATURED[collection_name]['center']
      template_values['center'] = '{lat:%s,lng:%s}' % (collection_center['lat'],
                                                       collection_center['lng'])
    scenes_json = list()
    for key in scene_keys:
      scenes_json.append(self.export_place_fields(
                        placedlit.PlacedLit().get(key)))
    template_values['scenes'] = json.dumps(scenes_json)
    self.render_template('map.tmpl', template_values)


class UpdateCatalanCollectionbyUserHandler(baseapp.BaseAppHandler):
  """ update catalan users """
  def get(self):
    logging.info('fixing catalan')
    place_query = db.GqlQuery(
        'SELECT __key__ FROM PlacedLit WHERE user_email = :1',
        'espaisescrits@gmail.com')
    collection = collections.Collection().get_named('catalan')
    for place in place_query:
      if place not in collection.scenes:
        logging.info('place added: %s', place)
        collection.scenes.append(place)
    collection.put()
    place_query = db.GqlQuery(
        'SELECT __key__ FROM PlacedLit WHERE user_email = :1',
        'fjoseppla@gmail.com')
    collection = collections.Collection().get_named('catalan')
    for place in place_query:
      if place not in collection.scenes:
        logging.info('place added: %s', place)
        collection.scenes.append(place)
    collection.put()


class UpdateSiteUserScenesHandler(baseapp.BaseAppHandler):
  def get(self):
    deferred.defer(update_schema.update_user_scene_data)
    self.response.out.write('Schema migration successfully initiated.')

handler_urls = [
  ('/collections/fix', UpdateCatalanCollectionbyUserHandler),
  ('/collections/users', UpdateSiteUserScenesHandler),
  ('/collections/(.*)', SceneCollectionHandler),
]

app = webapp.WSGIApplication(handler_urls, debug=True)
