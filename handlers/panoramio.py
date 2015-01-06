""" request handler for panaramio photos """
# pylint: disable=W0403, R0904, C0103


from google.appengine.ext import deferred
from google.appengine.ext import webapp


from classes import photo_index

import update_schema


class UpdatePhotosBatchHandler(webapp.RequestHandler):
  def get(self):
    deferred.defer(update_schema.update_photo_data)
    self.response.out.write('photo update successfully initiated.')


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
