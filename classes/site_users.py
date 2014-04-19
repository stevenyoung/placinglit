""" Datastore model for user data """
import logging

from google.appengine.ext import ndb


class User(ndb.Model):
  """ user properties """
  added_scenes = ndb.KeyProperty(repeated=True)
  visited_scenes = ndb.KeyProperty(repeated=True)

  @classmethod
  def create(cls, user_email):
    """ new User """
    logging.info('creating user %s', user_email)
    user = cls(id=user_email)
    user.put()
    logging.info('created user %s', user.key)
    return user

  def visit_scene(self, scene_key):
    """ updated list of visited scenes """
    logging.info('update scene visit %s', scene_key)
    # visit_key = ndb.Key(urlsafe=str(scene_key))
    # self.visited_scenes.append(visit_key)
    self.visited_scenes.append(ndb.Key.from_old_key(scene_key))
    self.put()
    logging.info('visit scene %s', self.key)

  def add_scene(self, scene_key):
    """ updated list of added scenes """
    self.added_scenes.append(scene_key)
    self.put()
    logging.info('add scene %s', self.key)

  def has_visited_scene(self, scene_key):
    """ scene checked in? """
    logging.info('visited? %s', scene_key)
    if ndb.Key.from_old_key(scene_key) in self.visited_scenes:
      return True
    else:
      return False

  def get_from_email(self, user_email):
    """ get site user by email """
    user = self.get_by_id(user_email)
    if not user:
      user = self.create(user_email)
    return user
