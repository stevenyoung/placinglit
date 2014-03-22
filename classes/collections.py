""" Datastore model for scene collections. """
#  pylint: disable=R0904, W0403

from google.appengine.ext import db


class Collection(db.Model):
  """ Collections of scenes """
  name = db.StringProperty()
  url = db.LinkProperty()
  scenes = db.ListProperty(db.Key)

  def add_scene(self, scene_key):
    self.scenes.append(scene_key)
    self.put()
