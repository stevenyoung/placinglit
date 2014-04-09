"""Import ISBN data """
# pylint: disable:C0103
import json
import logging

from google.appengine.ext import webapp

from handlers.abstracts import baseapp

from classes import books
from classes import authors


class ISBNdbBookImportHandler(baseapp.BaseAppHandler):
  """ Request handler for importing ISBN data."""
  def get(self):
    pass

  def post(self):
    json_data = json.loads(self.request.body)
    book_key = books.Book.create_from_json(json_data)
    if 'author_data' in json_data:
      for author_data in json_data['author_data']:
        author = authors.Author.get_by_key_name(author_data['id'])
        if book_key not in author.books:
          author.add_book(book_key)


class UpdateAuthorPropertyHandler(baseapp.BaseAppHandler):
  """ update author property"""
  def get(self):
    authors.Author.update_author_property()
    self.response.write('done')


urls = [
  ('/isbndb/book_import', ISBNdbBookImportHandler),
  ('/isbndb/author_update', UpdateAuthorPropertyHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
