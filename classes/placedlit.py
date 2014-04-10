""" Datastore model for scenes. """
# pylint: disable=W0403, R0904


from datetime import datetime
import itertools
import logging
import urlparse

from google.appengine.ext import db
from google.appengine.api import memcache

ALL_PLACES_LOCATION_KEY = 'show_all_places'

import books


class PlacedLit(db.Model):
  """ Scenes represented. """
  title = db.StringProperty()
  author = db.StringProperty()
  scenelocation = db.StringProperty()
  scenetime = db.StringProperty()
  actors = db.StringProperty()
  symbols = db.StringProperty()
  scenedescription = db.TextProperty()
  notes = db.StringProperty()
  ts = db.DateTimeProperty(required=True, auto_now_add=True)
  location = db.GeoPtProperty()
  checkins = db.IntegerProperty(required=True, default=0)
  image_url = db.LinkProperty()
  google_user = db.UserProperty()
  user_email = db.EmailProperty()
  book_data = db.ReferenceProperty(books.Book, collection_name='book')
  ug_isbn = db.StringProperty('')

  @classmethod
  def create_from_dict(cls, place_data):
    """ Scenes from users, web services"""
    placed = cls(
      title=place_data['title'],
      author=place_data['author'],
      scenelocation=place_data['place_name'],
      scenedescription=place_data['scene'],
      notes=place_data['notes'],
      google_user=place_data['user'],
      user_email=place_data['email'])
    placed.location = db.GeoPt(lat=place_data['latitude'],
                               lon=place_data['longitude'])

    if 'image_url' in place_data:
      image_url = urlparse.urlsplit(place_data['image_url'])
      if image_url.scheme and image_url.netloc:
        placed.image_url = urlparse.urlunsplit(image_url)

    if 'check_in' in place_data:
      placed.checkins += 1

    if 'current_checkin_count' in place_data:
      placed.checkins = place_data['current_checkin_count']

    if 'timestamp' in place_data:
      placed.ts = datetime.strptime(place_data['timestamp'], '%Y-%m-%d %X.%f')

    if 'ug_isbn' in place_data:
      placed.ug_isbn = place_data['ug_isbn']

    try:
      entity_key = placed.put()
      memcache.add(str(entity_key.id()), placed)
      return entity_key
    except db.BadValueError:
      logging.error('create/update error: {}'.format(place_data))

  @classmethod
  def get_place_from_id(cls, place_id):
    """ Get a scene given its id. """
    place = memcache.get(str(place_id))
    if place is None:
      place = cls.get_by_id(int(place_id))
      memcache.set(str(place_id), place)

    try:
      return place
    except AttributeError:
      logging.error('id {} could not be retrieved'.format(place_id))

  @classmethod
  def get_all_places(cls):
    """ Get them all. """
    all_places = memcache.get(ALL_PLACES_LOCATION_KEY)
    if all_places is None:
      all_places = cls.all()
      memcache.add(ALL_PLACES_LOCATION_KEY, all_places)
    return all_places

  @classmethod
  def get_newest_places(cls, limit=5):
    """ What's new? """
    return cls.all().order('-ts').run(limit=limit)

  @classmethod
  def count(cls):
    """ How many scenes have been added """
    return cls.all().count(limit=10000)

  def update_visit_count(self):
    """ Increment place visit count. """
    self.checkins += 1
    try:
      self.put()
      logging.info('update checkin info for: ' + str(self.key().id()))
      memcache.set(str(self.key().id()), self)
      return self.key()
    except db.BadValueError:
      logging.error('update visit count error - id:%s, count:%s',
                    self.key().id(), self.checkins)

  @classmethod
  def get_all_authors(cls):
    """ Get all authors. """
    try:
      pl_query = db.GqlQuery('SELECT DISTINCT author FROM PlacedLit')
      author_query = db.GqlQuery('SELECT DISTINCT author FROM Author')
      return itertools.chain(pl_query.run(), author_query.run())
    except:
      raise

  @classmethod
  def get_all_titles(cls):
    """" Get all titles. """
    try:
      pl_query = db.GqlQuery('SELECT DISTINCT title FROM PlacedLit')
      book_query = db.GqlQuery('SELECT DISTINCT title FROM Book')
      return itertools.chain(pl_query.run(), book_query.run())
    except:
      raise

  @classmethod
  def places_by_query(cls, field=None, term=None):
    """ Get scenes matching an arbitrary query. """
    try:
      place_query = cls.all().filter(field, term)
      places = place_query.run()
      return places
    except UnicodeDecodeError:
      logging.error('decode error! places by query: %s %s %s', field,
                    term, type(term))
      place_query = cls.all().filter(field, term.decode('iso-8859-1'))
      places = place_query.run()
      return places

  @classmethod
  def get_all_unresolved_places(cls):
    """ Get scenes that are missing book data """
    try:
      query = db.GqlQuery('SELECT * from PlacedLit WHERE book_data = NULL')
      return query.run()
    except:
      raise
