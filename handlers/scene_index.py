""" handle scene indexes """
from google.appengine.ext import webapp

from handlers.abstracts import baseapp
from classes import placedlit
from classes import scene_index


class SceneIndexHandler(webapp.RequestHandler):
  """ add all scenes to the index. """
  def get(self):
    query = placedlit.PlacedLit.all()
    for scene in query.run():
      scene_index.update_scene_index(scene.key().id())


class IndexInfoHandler(webapp.RequestHandler):
  """ get info on indexes """
  def get(self):
    indices = scene_index.get_index_info()
    self.response.write(indices)


class GetPlacesHandler(baseapp.BaseAppHandler):
  def get(self, query=None):
    lat = self.request.get('lat')
    lon = self.request.get('lon')
    places = placedlit.PlacedLit.get_nearby_places(lat, lon)
    loc_json = []
    for doc in places:
      place_dict = {'db_key': doc.doc_id}
      for field in doc.fields:
        if field.name == 'scene_location':
          place_dict['latitude'] = field.value.latitude
          place_dict['longitude'] = field.value.longitude
        else:
          place_dict[field.name] = field.value
      loc_json.append(place_dict)
    self.output_json(loc_json)


class EmptySceneIndexHandler(webapp.RequestHandler):
  def get(self):
    scene_index.delete_all_in_index('SceneIndex')


urls = [
  ('/scene_index/scenes', SceneIndexHandler),
  ('/scene_index/info', IndexInfoHandler),
  ('/scene_index/empty', EmptySceneIndexHandler),
  ('/places/near(/?.*)', GetPlacesHandler),
]

app = webapp.WSGIApplication(urls)
