""" request handler for panaramio photos """

import json
import urllib2

from google.appengine.ext import db
from google.appengine.ext import webapp

from handlers.abstracts import baseapp

from classes import panoramio


class UpdatePhotosHandler(baseapp.BaseAppHandler):
  def get(self):
    query = db.GqlQuery('SELECT __key__ from PlacedLit')
    for key in query.run(limit=10):
      url = panoramio.build_url_for_scene(scene_key=key)
      request = urllib2.Request(url)
      response = json.loads(urllib2.urlopen(request).read())
      photos = response['photos']
      map_location = None
      if 'map_location' in response:
        map_location = response['map_location']
      for photo in photos:
        panoramio.Panoramio.save_images_for_scene(scene_key=key, data=photo,
                                                  location=map_location)


urls = [('/photos/update_all', UpdatePhotosHandler)]

app = webapp.WSGIApplication(urls, debug=True)
