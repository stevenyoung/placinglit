import json

from google.appengine.ext import webapp

from handlers.abstracts import baseapp

from classes import books


class BooksHandler(baseapp.BaseAppHandler):
  def get(self, book_id):
    place = books.Book(book_id)
    pass

  def post(self, id=None):
    book_data = json.loads(self.request.body)
    book = books.Book.save(book_data)
    return book

urls = [
  ('/book/(.*)', BooksHandler)
]


app = webapp.WSGIApplication(urls, debug="True")
