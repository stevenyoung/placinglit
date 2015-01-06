""" Datastore model for user data """
from google.appengine.ext import ndb


class User(ndb.Model):
  """ user properties """
  email = ndb.StringProperty()
  added_scenes = ndb.KeyProperty(repeated=True)
  visited_scenes = ndb.KeyProperty(repeated=True)

  @classmethod
  def create(cls, user_email):
    """ new User """
    user = cls(id=user_email)
    user.email = user_email
    user.put()
    return user

  def visit_scene(self, scene_key):
    """ updated list of visited scenes """
    self.visited_scenes.append(ndb.Key.from_old_key(scene_key))
    self.put()

  def add_scene(self, scene_key):
    """ updated list of added scenes """
    self.added_scenes.append(ndb.Key.from_old_key(scene_key))
    self.put()

  def has_visited_scene(self, scene_key):
    """ scene checked in? """
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
