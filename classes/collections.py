""" Datastore model for scene collections. """
#  pylint: disable=R0904, W0403

from google.appengine.ext import db

FEATURED = dict()
FEATURED['catalan'] = {'url': 'http://www.espaisescrits.cat/',
                       'user': 'info@espaisescrits.cat'}
FEATURED['slq'] = {'url': 'http://slq.qld.gov.au',
                   'user': 'webmanager@slq.qld.gov.au'}


class Collection(db.Model):
  """ Collections of scenes """
  name = db.StringProperty()
  url = db.LinkProperty()
  scenes = db.ListProperty(db.Key)

  def add_scene(self, scene_key):
    """ add a scene to this collection """
    self.scenes.append(scene_key)
    self.put()

  def get_named(self, collection_name):
    """ collections are keyed by names or created if key is not found """
    collection = self.get_by_key_name(collection_name)
    if not collection:
      collection = Collection(key_name=collection_name)
      if collection_name in FEATURED:
        collection.url = FEATURED[collection_name]['url']
        collection.put()
    return collection
