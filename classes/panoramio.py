""" Datastore model for scene photos from panoramio. """
import logging

from google.appengine.ext import ndb

import placedlit


def build_url_for_scene(scene_key):
  """
  for "set" you can use:
    public (popular photos)
    full (all photos)
    user ID number

  for "size" you can use:
    original
    medium (default value)
    small
    thumbnail
    square
    mini_square

    minx, miny, maxx, maxy define the area to show photos from
    (minimum longitude, latitude, maximum longitude and latitude)

    number of photos to be displayed using "from=X" and "to=Y",
    where Y-X is the number of photos included.
    The value 0 represents the latest photo uploaded to Panoramio.
    "from=0 to=20" will extract a set of the last 20 photos uploaded to
    Panoramio, "from=20 to=40" the previous set of 20 photos and so on.
    The maximum number of photos you can retrieve in one query is 100.
  """
  scene = placedlit.PlacedLit.get(scene_key)
  distance = 0.005

  api_url = 'http://www.panoramio.com/map/get_panoramas.php?'
  api_url += 'set=public&from=0&to=20'

  min_lng = scene.location.lon - distance
  min_lat = scene.location.lat - distance
  max_lng = scene.location.lon + distance
  max_lat = scene.location.lat + distance

  api_url += '&minx={}&miny={}&maxx={}&maxy={}'.format(min_lng, min_lat,
                                                       max_lng, max_lat)
  api_url += '&size=medium&mapfilter=true'
  return api_url


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
