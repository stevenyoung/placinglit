from google.appengine.ext import deferred
from google.appengine.ext import webapp

import update_schema


class UpdateBooksHandler(webapp.RequestHandler):
  def get(self):
    deferred.defer(update_schema.update_book_data)
    self.response.out.write('Schema migration successfully initiated.')


class UpdateUserISBNHandler(webapp.RequestHandler):
  def get(self):
    deferred.defer(update_schema.update_schema)
    self.response.out.write('Schema migration successfully initiated.')


app = webapp.WSGIApplication([
  ('/update_books', UpdateBooksHandler),
  ('/update_isbns', UpdateUserISBNHandler),
  ])
