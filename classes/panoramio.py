""" Datastore model for scene photos from panoramio. """
# pylint: disable=W0403, R0904, C0103

import json
import urllib2

from google.appengine.ext import ndb

import photo_index
import placedlit


CORNER_DISTANCE = 0.005  # distance from lat, lng of scene
IMAGE_COUNT = 10


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

  api_url = 'http://www.panoramio.com/map/get_panoramas.php?'
  api_url += 'set=public&from=0&to={}'.format(IMAGE_COUNT)

  scene = placedlit.PlacedLit.get(scene_key)
  if scene:
    min_lng = scene.location.lon - CORNER_DISTANCE
    min_lat = scene.location.lat - CORNER_DISTANCE
    max_lng = scene.location.lon + CORNER_DISTANCE
    max_lat = scene.location.lat + CORNER_DISTANCE

    api_url += '&minx={}&miny={}&maxx={}&maxy={}'.format(min_lng, min_lat,
                                                         max_lng, max_lat)
    api_url += '&size=medium&mapfilter=true'
    return api_url
  else:
    return None


def get_api_data(url):
    request = urllib2.Request(url)
    response = json.loads(urllib2.urlopen(request).read())
    return response


def get_photos_for_scene(scene_key):
  """ get photos associated with a scene """
  query_key = ndb.Key.from_old_key(scene_key)
  query = Panoramio.query().filter(Panoramio.PLscene == query_key)
  if len(query.fetch()) < 1:
    return None
  photos = [result for result in query.fetch()]
  return photos


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
    scene_id = scene_key.id()
    photo_index.add_scene_to_panoramio_index(scene_id,
                                             data['photo_id'],
                                             data['owner_id'])
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
    if location:
      image.map_location = ndb.GeoPt(lat=location['lat'], lon=location['lon'])
    image.put()
