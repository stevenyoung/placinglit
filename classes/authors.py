"""
Datastore model for authors.
And methods for standardizing author names from disparate sources.
User entry and isbndb crowd-sourced data often has
"""

import logging

from google.appengine.ext import db


def format_author_names(author_name):
  """ Parse string for first and last names. """
  first_name = ''
  last_name = ''
  if ',' in author_name:
    last_name, first_name = author_name.split(',')
  elif ' ' in author_name:
    first_name, last_name = author_name.split(' ', 1)
  else:
    first_name = author_name
  last_name = last_name.strip()
  first_name = first_name.strip()
  return first_name, last_name


class Author(db.Model):   # pylint: disable=R0904
  """ Author representation """
  author_id = db.StringProperty()
  first_name = db.StringProperty()
  last_name = db.StringProperty()
  books = db.ListProperty(db.Key)
  display_name = db.StringProperty()
  source = db.StringProperty()
  author = db.StringProperty()

  @classmethod
  def get_author_key(cls, author_json=None, author_id=None):
    """ Get author db.Key for reference properties
        args:
          author_json: author data in json format
          author_id: author id 'first_last'
        returns:
          author_key: db.Key of new/existing author
    """
    if author_json:
      author_id = author_json['id']
    if author_id:
      author_query = Author.all().filter('author_id =', author_id)
      result = author_query.get()
    if result:
      return result.key()
    else:
      author_key = cls.create_from_json(author_json)
      return author_key

  @classmethod
  def create_from_json(cls, author_json, source="isbndb"):
    """ new author from json """
    logging.info('author create from json %s', author_json)
    first_name, last_name = (format_author_names(author_json['name']))
    display_name = ' '.join([first_name, last_name])
    author_id = author_json['id']
    author = cls(
      key_name=author_id,
      author_id=author_id,
      first_name=first_name,
      last_name=last_name,
      display_name=display_name,
      source=source,
      author=display_name
      )
    author.books = list()
    try:
      author_key = author.put()
      return author_key
    except ValueError:
      logging.error('cannot add author %s', author_json)

  def add_book(self, book_key):
    """ Add a books db.Key to an author. """
    self.books.append(book_key)
    self.put()

  @classmethod
  def get_by_author_id(cls, author_id):
    """" Get by author  from author id """
    author_query = cls.all().filter('author_id =', author_id)
    results = author_query.run(limit=1)
    return results

  @classmethod
  def update_author_property(cls):
    """ make sure 'author' is the same as 'display_name' """
    author_query = cls.all()
    to_put = list()
    for author in author_query.run():
      logging.info(author.display_name)
      author.author = author.display_name
      to_put.append(author)
    db.put(to_put)
