""" request handler for panaramio photos """

import json
import logging
import urllib2

from google.appengine.ext import db
from google.appengine.ext import webapp

from handlers.abstracts import baseapp

from classes import panoramio
from classes import placedlit

ISBNDB_API_KEY = 'SVJOWP23'
ISBNDB_API_URL = 'http://isbndb.com/api/v2/json'

# def build_url_for_scene(scene_key):

#   scene = placedlit.PlacedLit.get(scene_key)

#   return api_url


# def get_api_data(url):
#     request = urllib2.Request(url)
#     response = json.loads(urllib2.urlopen(request).read())
#     return response

def query_isbndb(query_term, query_type='book'):
  """ Query ISBNdb for a search term.
      args:
        query_term: string
        query_type: string 'book', 'author'
      returns:
        json response from ISBNdb
  """
  request_url = '/'.join([ISBNDB_API_URL, ISBNDB_API_KEY, query_type,
                          query_term])
  print(request_url)
  request = urllib2.Request(request_url)
  response = json.loads(urllib2.urlopen(request).read())
  update_request_list(query_term, query_term)
  return response

class UpdateTitleISBNdbDataHandler(baseapp.BaseAppHandler):
  def get(self, scene_id):
    key = db.Key.from_path('PlacedLit', scene_id)
    panoramio_data = get_api_data(panoramio.build_url_for_scene(scene_key=key))
    photos = panoramio_data['photos']
    map_location = None
    if 'map_location' in panoramio_data:
      map_location = panoramio_data['map_location']
    for photo in photos:
        panoramio.Panoramio.save_images_for_scene(scene_key=key, data=photo,
                                                  location=map_location)


class UpdateAllPhotosHandler(baseapp.BaseAppHandler):
  """ get panaramio photos for scenes without photos """
  def get(self):
    scene_query = db.GqlQuery('SELECT __key__ from PlacedLit')
    for key in scene_query.run():
      url = build_url_for_scene(scene_key=key)
      request = urllib2.Request(url)
      response = json.loads(urllib2.urlopen(request).read())
      photos = response['photos']
      map_location = None
      if 'map_location' in response:
        map_location = response['map_location']
      for photo in photos:
        panoramio.Panoramio.save_images_for_scene(scene_key=key, data=photo,
                                                  location=map_location)


urls = [
  ('/photos/panoramio/update_all', UpdateAllPhotosHandler),
  ('/photos/panoramio/(.*)', UpdateScenePhotoHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
