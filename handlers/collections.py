""" Handle web requests for collections """
# pylint disable=C0103
import json

from google.appengine.ext import webapp

from handlers.abstracts import baseapp

from classes import collections
from classes import placedlit


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

handler_urls = [('/collections/(.*)', SceneCollectionHandler)]

app = webapp.WSGIApplication(handler_urls, debug=True)
