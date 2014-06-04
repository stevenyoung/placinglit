""" handle scene location indexes """
from string import capwords

from google.appengine.ext import webapp

from handlers.abstracts import baseapp
from classes import location_index
from classes import placedlit


class BatchUpdateLocationsIndexHandler(webapp.RequestHandler):
  """ add all scenes to the index. """
  def get(self):
    location_index.batch_update_all_scenes()
    self.response.out.write('document index update successfully initiated.')


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
    self.response.out.write(indices)


class EmptySceneLocationIndexHandler(webapp.RequestHandler):
  """ removing scene location indexes """
  def get(self):
    location_index.empty_scene_index()
    self.response.out.write('tried to empty scene index')


class NearbyPlacesHandler(baseapp.BaseAppHandler):
  """ get places nearby """
  def get(self, query=None):
    lat = self.request.get('lat')
    lon = self.request.get('lon')
    places = location_index.sorted_location_query(lat, lon)
    formatted_results = self.format_location_index_results(places)
    self.output_json(formatted_results)


class NewestPlacesHandler(baseapp.BaseAppHandler):
  """ get newest places """
  def get(self, query=None):
    places = location_index.date_query()
    formatted_results = self.format_location_index_results(places)
    output = list()
    for result in formatted_results:
      scene = placedlit.PlacedLit.get_place_from_id(result['db_key'])
      result['location'] = capwords(scene.scenelocation)
      # logging.info('result: %s', result)
      output.append(result)
    # self.output_json(formatted_results)
    self.output_json(output)


urls = [
  ('/location_index/update_scenes', BatchUpdateLocationsIndexHandler),
  ('/location_index/info', IndexInfoHandler),
  ('/location_index/empty', EmptySceneLocationIndexHandler),
  ('/places/near(/?.*)', NearbyPlacesHandler),
  ('/places/latest(/?.*)', NewestPlacesHandler)
]

app = webapp.WSGIApplication(urls)
