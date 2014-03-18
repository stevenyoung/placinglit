""" Datastore model for scene collections. """
#  pylint: disable=R0904, W0403

from google.appengine.ext import db


@db.transactional(xg=True)
def add_scene(place_key):
  """ add scene """
  collection = Collection.get_or_insert(key_name='QLD')
  collection.scenes.append(place_key)
  collection.put()
  name = collection.key().name()
  print collection.key().name()
  assert name == "QLD"


class Collection(db.Model):
  """ Collections of scenes """

  name = db.StringProperty()
  url = db.LinkProperty()
  scenes = db.ListProperty(db.Key)

  def __init__(self, key_name=None):
    self.key_name = key_name
    super(Collection, self).__init__()
