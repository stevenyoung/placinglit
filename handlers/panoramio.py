""" request handler for panaramio photos """

import json
import logging
import urllib2

from google.appengine.ext import db
from google.appengine.ext import webapp

from handlers.abstracts import baseapp

from classes import panoramio
from classes import photo_index
from classes import placedlit


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

  distance = 0.005
  count = 10

  api_url = 'http://www.panoramio.com/map/get_panoramas.php?'
  api_url += 'set=public&from=0&to={}'.format(count)

  scene = placedlit.PlacedLit.get(scene_key)
  if scene:
    logging.info('scene: %s %s', scene_key, scene)

    min_lng = scene.location.lon - distance
    min_lat = scene.location.lat - distance
    max_lng = scene.location.lon + distance
    max_lat = scene.location.lat + distance

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


class UpdateScenePhotoHandler(baseapp.BaseAppHandler):
  def get(self, scene_id):
    key = db.Key.from_path('PlacedLit', scene_id)
    panoramio_data = get_api_data(build_url_for_scene(scene_key=key))
    if panoramio_data:
      photos = panoramio_data['photos']
      map_location = None
      if 'map_location' in panoramio_data:
        map_location = panoramio_data['map_location']
      for photo in photos:
          panoramio.Panoramio.save_images_for_scene(scene_key=key, data=photo,
                                                    location=map_location)


class UpdateAllPhotosHandler(baseapp.BaseAppHandler):
  """ get panaramio photos for scenes without photos """
  def get(self):
    scene_query = db.GqlQuery('SELECT __key__ from PlacedLit')
    scene_count = 0
    photo_count = 0
    for key in scene_query.run():
      if not photo_index.has_panoramio_photos(key.id()):
        url = build_url_for_scene(scene_key=key)
        request = urllib2.Request(url)
        response = json.loads(urllib2.urlopen(request).read())
        photos = response['photos']
        map_location = None
        if 'map_location' in response:
          map_location = response['map_location']
        for photo in photos:
          photo_count += 1
          panoramio.Panoramio.save_images_for_scene(scene_key=key, data=photo,
                                                    location=map_location)
        scene_count += 1
        logging.info('%s pix for %s scenes', photo_count, scene_count)

urls = [
  ('/photos/panoramio/update_all', UpdateAllPhotosHandler),
  ('/photos/panoramio/(.*)', UpdateScenePhotoHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
