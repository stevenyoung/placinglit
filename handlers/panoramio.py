""" request handler for panaramio photos """
# pylint: disable=W0403, R0904, C0103

import logging

from google.appengine.ext import db
from google.appengine.ext import deferred
from google.appengine.ext import webapp

from handlers.abstracts import baseapp

from classes import panoramio
from classes import photo_index

import update_schema


class UpdatePhotosBatchHandler(webapp.RequestHandler):
  def get(self):
    deferred.defer(update_schema.update_photo_data)
    self.response.out.write('Schema migration successfully initiated.')


class UpdateAllPhotosHandler(baseapp.BaseAppHandler):
  """ get panaramio photos for scenes without photos """
  def get(self):
    scene_query = db.GqlQuery('SELECT __key__ from PlacedLit')
    scene_count = 0
    photo_count = 0
    for key in scene_query.run():
      if photo_index.has_panoramio_photos(key.id()):
        logging.info('%s already has photos', key.id())
      else:
        url = panoramio.build_url_for_scene(scene_key=key)
        api_response = panoramio.get_api_data(url)
        if 'map_location' in api_response:
          map_location = api_response['map_location']
          for photo in api_response['photos']:
            photo_count += 1
            panoramio.Panoramio.save_images_for_scene(scene_key=key, data=photo,
                                                      location=map_location)
      scene_count += 1
    logging.info('added %s pix for %s scenes', photo_count, scene_count)


class EmptyPhotoIndexHandler(webapp.RequestHandler):
  """ empty photo index """
  def get(self):
    photo_index.empty_panoramio_index()


class PhotoIndexInfoHandler(webapp.RequestHandler):
  """ index info """
  def get(self):
    photo_index.index_info()


handler_urls = [
  # ('/photos/panoramio/update_all', UpdateAllPhotosHandler),
  ('/photos/panoramio/update_all', UpdatePhotosBatchHandler),
  ('/photos/panoramio/empty', EmptyPhotoIndexHandler),
  ('/photos/panoramio/info', PhotoIndexInfoHandler)
]

app = webapp.WSGIApplication(handler_urls, debug=True)
