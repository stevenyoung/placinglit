""" Datastore model for scenes. """
# pylint: disable=W0403, R0904, C0103


from datetime import datetime
import itertools
import logging
import random
import urlparse

from google.appengine.ext import db
from google.appengine.api import memcache

ALL_PLACES_LOCATION_KEY = 'show_all_places'

import books
import site_users
import panoramio
import location_index


def get_nearby_places(lat, lon, sorted_by_distance=False):
  """ run location query """
  if sorted_by_distance:
    return location_index.sorted_location_query(lat, lon)
  else:
    return location_index.location_query(lat, lon)


def get_search_doc_for_scene(scene_id):
  """ get fod from index by id """
  return location_index.get_document_for_scene(scene_id)


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
      if place_data['check_in']:
        placed.checkins = 1

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

  def update_visit_count(self, user_email):
    """ Increment place visit count. """
    scene_key = self.key()
    visitor = site_users.User().get_from_email(user_email)
    # checkins = None
    visited = visitor.has_visited_scene(scene_key)
    if not visited:
      visitor.visit_scene(scene_key)
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
      user_authors = set([result.author for result in pl_query.run()])
      isbndb_authors = set([result.author for result in author_query.run()])
      author_list = list()
      for author in user_authors.union(isbndb_authors):
        author_list.append({'author': author})
      return author_list
    except:
      raise

  @classmethod
  def get_all_titles(cls):
    """" Get all titles. """
    try:
      pl_query = db.GqlQuery('SELECT DISTINCT title FROM PlacedLit')
      book_query = db.GqlQuery('SELECT DISTINCT title FROM Book')
      user_titles = set([result.title for result in pl_query.run()])
      isbndb_titles = set([result.title for result in book_query.run()])
      title_list = list()
      for title in user_titles.union(isbndb_titles):
        title_list.append({'title': title})
      return title_list
    except:
      raise

  @classmethod
  def places_by_query(cls, field=None, term=None):
    """ Get scenes matching an arbitrary query. """
    if field == 'author':
      places = location_index.author_query(author_name=term)
    else:
      try:
        place_query = cls.all().filter(field, term)
        places = place_query.run()
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

  def update_fields(self, updated_data):
    # poorly formed urls raise db.Error.BadValueError for db.LinkProperty
    image_url = urlparse.urlsplit(updated_data['image_url'])
    if image_url.scheme and image_url.netloc:
      self.image_url = urlparse.urlunsplit(image_url)
    else:
      self.image_url = None

    for field in updated_data.iterkeys():
      if field is not 'image_url':
        setattr(self, field, updated_data[field])

    self.put()
    memcache.set(str(self.key().id()), self)

  def delete_scene(self):
    scene_id = str(self.key().id())
    memcache.delete(scene_id)
    self.delete()
    flushed = memcache.flush_all()
    logging.info('deleted %s. flushed:%s', scene_id, flushed)

  def get_image_data(self):
    images = panoramio.get_photos_for_scene(self.key())
    if not images:
      return None
    image = random.choice(images)
    return {'photo_id': image.photo_id, 'owner': image.owner_id}
