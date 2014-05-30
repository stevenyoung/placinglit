# import json
""" update scenes """
import logging

from google.appengine.ext import deferred
from google.appengine.ext import db
from google.appengine.ext import ndb

from classes import placedlit
from classes import books
from classes import site_users

from classes import panoramio
from classes import photo_index

DB_BATCH_SIZE = 50  # ideal batch size may vary based on entity size.
INDEX_BATCH_SIZE = 200
TITLE_ISBNS = dict()


def transform_author_name_for_query(name):
  """ author id is formatted last_first """
  if ' ' in name:
    first, last = name.rsplit(' ', 1)
    query_name = (last + ' ' + first).lower().replace(' ', '_')
  else:
    query_name = name.lower()
  return query_name


def update_user_scene_data(cursor=None, num_updated=0):
  """ add scenes to site users """
  scene_query = placedlit.PlacedLit.all()
  if cursor:
    scene_query.with_cursor(cursor)

  users_to_put = list()
  for scene in scene_query.fetch(limit=500):
    if scene.user_email:
      logging.debug('email %s', scene.user_email)
      user = site_users.User.get_by_id(scene.user_email)
      if not user:
        user = site_users.User.create(scene.user_email)
      user.email = scene.user_email
      user.added_scenes.append(ndb.Key.from_old_key(scene.key()))
      users_to_put.append(user)

  if users_to_put:
    ndb.put_multi(users_to_put)
    num_updated += len(users_to_put)
    logging.debug('Put %d entities to Datastore for a total of %d',
                  len(users_to_put), num_updated)
    deferred.defer(update_user_scene_data, cursor=scene_query.cursor(),
                   num_updated=num_updated)
  else:
    logging.debug('Update user scenes complete with %d updates!', num_updated)


def update_book_data(cursor=None, num_updated=0):
  """ Set ISBNdb reference for places """
  query = placedlit.PlacedLit.all()
  if cursor:
    query.with_cursor(cursor)

  to_put = []
  for place in query.fetch(limit=DB_BATCH_SIZE):
    place.ISBNdb = None
    query_title = place.title.lower().replace(' ', '_')
    query_author = transform_author_name_for_query(place.author)
    logging.info('%s by %s?', query_title, query_author)
    # matching books and authors
    matching_books = books.Book.get_by_key_name(query_title)
    if matching_books:
      for index, book in enumerate(matching_books.authors):
        author_name = matching_books.authors[index].name()
        if author_name == query_author:
          place.book_data = matching_books
          # to_put.append(place)
          logging.info('found %s by %s', query_title, query_author)
    to_put.append(place)

    # matching book titles only
    # matching_book = books.Book.get_by_key_name(query_title)
    # if matching_book:
    #   print matching_book.title
    #   place.book_data = matching_book
    #   to_put.append(place)

  if to_put:
    db.put(to_put)
    num_updated += len(to_put)
    logging.debug(
      'Put %d entities to Datastore for a total of %d',
      len(to_put), num_updated)
    deferred.defer(
      update_book_data, cursor=query.cursor(), num_updated=num_updated)
  else:
    logging.debug('UpdateSchema complete with %d updates!', num_updated)


def update_photo_data(cursor=None, num_updated=0, previous_cursor=None):
  """
  Get photos for scenes lacking photos.
  This is done by getting all scenes in a cursored query, iterating through the
  scenes and querying the Panoramio API with the scene's location data.
  This will create a number of Panoramio entities for each scene as well as a
  search.Document for the photo_index for each photo.
  """
  query = placedlit.PlacedLit.all(keys_only=True)
  if cursor:
    query.with_cursor(cursor)

  to_put = []
  for key in query.fetch(limit=INDEX_BATCH_SIZE):
    # scene_id = place.key().id()
    scene_id = key.id()
    if photo_index.has_panoramio_photos(scene_id):
        logging.debug('%s already has photos', scene_id)
    else:
      # api_url = panoramio.build_url_for_scene(place.key())
      api_url = panoramio.build_url_for_scene(key)
      api_response = panoramio.get_api_data(api_url)
      if 'map_location' in api_response:
        map_location = api_response['map_location']
        for photo in api_response['photos']:
          image = panoramio.Panoramio()
          image.id = photo['photo_id']
          # image.PLscene = ndb.Key.from_old_key(place.key())
          image.PLscene = ndb.Key.from_old_key(key)
          image.photo_id = photo['photo_id']
          image.photo_title = photo['photo_title']
          image.photo_url = photo['photo_url']
          image.photo_file_url = photo['photo_file_url']
          image.width = photo['width']
          image.height = photo['height']
          image.owner_id = photo['owner_id']
          image.owner_name = photo['owner_name']
          image.owner_url = photo['owner_url']
          image.map_location = ndb.GeoPt(lat=map_location['lat'],
                                         lon=map_location['lon'])

          num_updated += 1
          to_put.append(image)

  if to_put:
    ndb.put_multi(to_put)
    for image in to_put:
      db_key = image.PLscene.to_old_key()
      photo_index.add_scene_to_panoramio_index(db_key.id(),
                                               image.id,
                                               image.owner_id)
    num_updated += len(to_put)
    logging.debug(
      'Put %d entities to Datastore for a total of %d',
      len(to_put), num_updated)
  previous_cursor = cursor

  if previous_cursor != query.cursor():
    deferred.defer(
      update_photo_data,
      cursor=query.cursor(),
      num_updated=num_updated,
      previous_cursor=previous_cursor)
  else:
    logging.debug('photo update complete with %d updates!', num_updated)
