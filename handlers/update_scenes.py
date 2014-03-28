from google.appengine.ext import db
from google.appengine.ext import deferred
from google.appengine.ext import webapp

import update_schema


class UpdateBooksHandler(webapp.RequestHandler):
  def get(self):
    deferred.defer(update_schema.update_book_data)
    self.response.out.write('Schema migration successfully initiated.')


class ResetUserISBNHandler(webapp.RequestHandler):
  def get(self):
    isbn_query = db.GqlQuery('SELECT * from PlacedLit WHERE ug_isbn = :1', '')
    scene_list = list()
    for scene in isbn_query:
      scene.ug_isbn = None
      scene_list.append(scene)
    db.put(scene_list)
    self.response.out.write(' done.')


class UpdateUserISBNHandler(webapp.RequestHandler):
  def get(self):
    # deferred.defer(update_schema.update_user_isbns)
    self.response.out.write('isbn update successfully initiated.<br/>')
    place_query = db.GqlQuery('SELECT * FROM PlacedLit WHERE ug_isbn != :1',
                              None)
    title_isbns = dict()
    to_put = list()
    for place in place_query:
      title_isbns[place.title] = place.ug_isbn

    # print title_isbns
    self.response.out.write('count: {}<br/>'.format(len(title_isbns)))
    for title, isbn in title_isbns.iteritems():
      # self.response.out.write('{}:{}<br/>'.format(title, isbn))
      self.response.out.write('{}<br/>'.format(isbn))
      title_query = db.GqlQuery(
        'SELECT * from PlacedLit WHERE title = :1 AND ug_isbn = :2',
        title, None)
      for scene in title_query:
        scene.ug_isbn = isbn
        to_put.append(scene)
        # self.response.out.write('updating {} ({})</br>'.format(title, isbn))
    db.put(to_put)
    self.response.out.write(' done.')


app = webapp.WSGIApplication([
  ('/update_books', UpdateBooksHandler),
  ('/update_isbns', UpdateUserISBNHandler),
  ('/reset_isbns', ResetUserISBNHandler)
  ])
