__author__ = 'steven@eyeballschool.com (Steven)'

from google.appengine.ext import db
from classes import placedlit


class UserRequest(db.Expando):
  ua = db.StringProperty()
  user_loc = db.ReferenceProperty(placedlit.PlacedLit)

  @classmethod
  def create(cls, ua=None, user_loc=None):
    req = cls(ua=ua, user_loc=user_loc)
    req.put()
    return req.key()
