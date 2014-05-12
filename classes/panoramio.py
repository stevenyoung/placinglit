""" Datastore model for scene photos from panoramio. """
import logging

from google.appengine.ext import ndb


def retrieved_scenes():
  """ List of scene for which we already have photo data. """
  # return PanoramioScenes.scenes
  return None


def get_photos_for_scene(scene_key):
  query_key = ndb.Key.from_old_key(scene_key)
  query = Panoramio.query().filter(Panoramio.PLscene == query_key)
  if len(query.fetch()) < 1:
    return None
  photos = [result for result in query.fetch()]
  return photos


class PanoramioScenes(ndb.Model):
  """
    scenes: list of scenes that have photos
    photo_ids: list of photo_ids
  """
  scenes = ndb.KeyProperty(repeated=True)
  photo_ids = ndb.IntegerProperty(repeated=True)
  owner_ids = ndb.IntegerProperty(repeated=True)


class Panoramio(ndb.Expando):
  """ panoramio result format """
  PLscene = ndb.KeyProperty()
  photo_id = ndb.IntegerProperty()
  photo_title = ndb.StringProperty()
  photo_url = ndb.StringProperty()
  photo_file_url = ndb.StringProperty()
  photo_location = ndb.GeoPtProperty()
  width = ndb.IntegerProperty()
  height = ndb.IntegerProperty()
  owner_id = ndb.IntegerProperty()
  owner_name = ndb.StringProperty()
  owner_url = ndb.StringProperty()
  map_location = ndb.GeoPtProperty()

  @classmethod
  def save_images_for_scene(cls, scene_key=None, data=None, location=None):
    """ save an image from an api response. """
    # location = data['map_location']
    # count = data['count']
    query_key = ndb.Key.from_old_key(scene_key)
    # scene_data = PanoramioScenes(scenes=query_key)
    image = cls(
      id=data['photo_id'],
      PLscene=query_key,
      photo_id=data['photo_id'],
      photo_title=data['photo_title'],
      photo_url=data['photo_url'],
      photo_file_url=data['photo_file_url'],
      width=data['width'],
      height=data['height'],
      owner_id=data['owner_id'],
      owner_name=data['owner_name'],
      owner_url=data['owner_url'],
    )
    # scene_data.photo_ids = data['photo_id']
    # scene_data.owner_ids = data['owner_id']
    # scene_data.put()
    if location:
      image.map_location = ndb.GeoPt(lat=location['lat'], lon=location['lon'])
    image.put()
