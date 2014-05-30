__author__ = 'steven@eyeballschool.com (Steven)'

import logging

from google.appengine.ext import db


class PlacedLit(db.Expando):
  title = db.StringProperty()
  author = db.StringProperty()
  scenelocation = db.StringProperty()
  scenetime = db.StringProperty()
  actors = db.StringProperty()
  symbols = db.StringProperty()
  scenedescription = db.StringProperty()
  notes = db.StringProperty()
  ts = db.DateTimeProperty(required=True, auto_now_add=True)
  location = db.GeoPtProperty()
  checkins = db.IntegerProperty(required=True, default=0)
  image_url = db.LinkProperty()
  google_user = db.UserProperty()

  @classmethod
  def create_or_update_from_dict(cls, place_data):
    placed = cls(
      title=place_data['title'],
      author=place_data['author'],
      scenelocation=place_data['place_name'],
      scenetime=place_data['date'],
      actors=place_data['actors'],
      symbols=place_data['symbols'],
      scenedescription=place_data['scene'],
      notes=place_data['notes'],
      google_user=place_data['user'])
    placed.location = db.GeoPt(lat=place_data['latitude'],
                               lon=place_data['longitude'])
    if place_data['image_url']:
      if not place_data['image_url'].startswith('http://'):
        place_data['image_url'] = 'http://' + place_data['image_url']
      placed.image_url = place_data['image_url']
    if place_data['check_in']:
      placed.checkins += 1
    try:
      placed.put()
      return placed.key()
    except db.BadValueError:
      logging.info('create/update error: %s' % place_data)

  @classmethod
  def get_place_from_id(cls, place_id):
    place = cls.get_by_id(int(place_id))
    try:
      return place
    except AttributeError:
      logging.info('id %s could not be retrieved' % place_id)

  @classmethod
  def get_all_places(cls):
    places = cls.all()
    return places

  @classmethod
  def get_newest_places(cls, limit=5):
    return cls.all().order('-ts').fetch(limit=limit)

  @classmethod
  def count(cls):
    return cls.all().count()

  def update_visit_count(self):
    self.checkins += 1
    try:
      self.put()
      return self.key()
    except db.BadValueError:
      logging.info('update visit count id:%s, count:%s', self.key().id(),
                   self.checkins)