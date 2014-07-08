""" Datastore models for book data."""

import json
import logging

from string import capwords

from google.appengine.ext import db

import authors


def get_author_from_json(author_json):
  """ Get author key """
  author_key = authors.Author.get_author_key(author_json=author_json)
  return author_key


class Book(db.Model):   # pylint: disable=R0904
  """ Represents ISBNdb query results for a title."""
  isbn10 = db.StringProperty()
  isbn13 = db.StringProperty()
  summary = db.TextProperty()
  lcc_number = db.StringProperty()
  subject_ids = db.StringListProperty()
  language = db.StringProperty()
  publisher = db.StringProperty()
  timestamp = db.DateTimeProperty(required=True, auto_now_add=True)
  title = db.StringProperty()
  book_id = db.StringProperty()
  source = db.StringProperty()
  authors = db.ListProperty(db.Key)

  @classmethod
  def create_from_json(cls, json_data, data_source='isbndb'):
    """ New instance from json. """
    book_data = cls(
      key_name=json_data['book_id'],
      isbn10=json_data['isbn10'],
      isbn13=json_data['isbn13'],
      lcc_number=json_data['lcc_number'],
      summary=json_data['summary'],
      book_id=json_data['book_id'],
      author_data=json.dumps(json_data['author_data']),
      publisher=json_data['publisher_text'],
      )
    book_data.authors = list()
    author_data = json_data['author_data']
    for author in author_data:
      author_key = get_author_from_json(author_json=author)
      book_data.authors.append(author_key)
    book_data.source = data_source
    book_data.title = capwords(json_data['title'])
    book_data.subject_ids = [subject for subject in json_data['subject_ids']]
    try:
      book_key = book_data.put()
      return book_key
    except db.BadValueError:
      logging.error('isbn create/update error: {}'.format(book_data))
