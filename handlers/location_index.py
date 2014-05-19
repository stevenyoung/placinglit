""" handle scene location indexes """
import logging

from google.appengine.ext import webapp

from handlers.abstracts import baseapp
from classes import placedlit
from classes import location_index
from classes import panoramio


class UpdateSceneLocationIndexHandler(webapp.RequestHandler):
  """ add all scenes to the index. """
  def get(self):
    query = placedlit.PlacedLit.all()
    for scene in query.run():
      location_index.update_scene_index(scene.key().id())


class IndexInfoHandler(webapp.RequestHandler):
  """ get info on indexes """
  def get(self):
    indices = location_index.get_index_info()
    self.response.write(indices)


class EmptySceneLocationIndexHandler(webapp.RequestHandler):
  """ removing scene location indexes """
  def get(self):
    location_index.delete_all_in_index()


class GetPlacesHandler(baseapp.BaseAppHandler):
  """ get places nearby """
  def get(self, query=None):
    lat = self.request.get('lat')
    lon = self.request.get('lon')
    places = placedlit.PlacedLit.get_nearby_places(lat, lon)
    loc_json = []
    for doc in places:
      place_dict = {'db_key': doc.doc_id}
      photo_id = panoramio.get_photos_for_scene(doc.doc_id)
      logging.info('photo %s', photo_id)
      for field in doc.fields:
        if field.name == 'scene_location':
          place_dict['latitude'] = field.value.latitude
          place_dict['longitude'] = field.value.longitude
        else:
          place_dict[field.name] = field.value
      loc_json.append(place_dict)
    self.output_json(loc_json)


urls = [
  ('/location_index/update_scenes', UpdateSceneLocationIndexHandler),
  ('/location_index/info', IndexInfoHandler),
  ('/location_index/empty', EmptySceneLocationIndexHandler),
  ('/places/near(/?.*)', GetPlacesHandler),
]

app = webapp.WSGIApplication(urls)
