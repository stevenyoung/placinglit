""" Datastore model for scene location documents """
# pylint: disable=W0403, R0904, C0103

import datetime
import logging

from google.appengine.api import search
from google.appengine.ext import deferred

import placedlit


INDEX_NAME = 'LocationIndex'
default_distance = 804500  # 500 miles, ~ map zoom level 6
sort_distance = default_distance + 1
result_limit = 500
BATCH_SIZE = 200


def author_query(author_name=None):
  query_string = 'author = \"{}\"'.format(author_name)
  doc_index = search.Index(name=INDEX_NAME)
  options = search.QueryOptions(limit=result_limit)
  query = search.Query(query_string=query_string, options=options)
  results = doc_index.search(query)
  return results


def get_index_info():
  indices = list()
  for index in search.get_indexes(fetch_schema=True):
    logging.info("index %s", index.name)
    logging.info("schema: %s", index.schema)
    indices.append({'name': index.name, 'schema': index.schema})
    doc_index = search.Index(name=index.name)
    docs = doc_index.get_range()
    for doc in docs:
      logging.info('%s:%s', doc['scene_location'], doc.doc_id)
  return indices


def empty_scene_index(index_name=INDEX_NAME):
  """ Delete all the docs in this index. Docs are deleted in batches of 100. """
  doc_index = search.Index(name=index_name)

  # looping because get_range by default returns up to 100 documents at a time
  while True:
  # Get a list of documents populating only the doc_id field and extract the ids
    document_ids = [document.doc_id
                    for document in doc_index.get_range(ids_only=True)]
    if not document_ids:
      break
    # Delete the documents for the given ids from the Index.
    doc_index.delete(document_ids)


def date_query(index_name=INDEX_NAME):
  doc_index = search.Index(name=index_name)
  query_date = datetime.datetime.now().date()
  logging.info('query date %s', query_date)
  query_string = 'date_added < {}'.format(query_date)
  logging.info('query string %s', query_string)
  expr_list = search.SortExpression(expression='date_added',
                                    default_value=query_date,
                                    direction=search.SortExpression.DESCENDING)
  date_sort = search.SortOptions(expressions=[expr_list])
  query = search.Query(query_string=query_string,
                       options=search.QueryOptions(limit=10,
                                                   sort_options=date_sort))
  results = doc_index.search(query)
  logging.info(len(results.results))
  logging.info(results.results)
  return results.results


def _do_proximity_query(query):
  index = search.Index(name=INDEX_NAME)
  try:
    results = index.search(query)
    total_matches = results.number_found
    number_of_docs_returned = len(results.results)
    logging.info('%s locations found', results.number_found)
    logging.info('%s total matches found', total_matches)
    logging.info('%s docs returned', number_of_docs_returned)
    return results.results
  except search.Error:
    logging.exception('Search failed')


def location_query(lat, lon, distance=default_distance):
  query_format = 'distance(scene_location, geopoint({}, {})) < {}'
  query_string = query_format.format(lat, lon, distance)
  query_options = search.QueryOptions(limit=result_limit)
  query = search.Query(query_string=query_string, options=query_options)
  return _do_proximity_query(query)


def sorted_location_query(lat, lon, distance=default_distance):
  query_format = 'distance(scene_location, geopoint({}, {})) < {}'
  query_string = query_format.format(lat, lon, distance)
  location_sort_expr_format = 'distance(scene_location, geopoint({}, {}))'
  location_sort_expr = location_sort_expr_format.format(lat, lon)
  sort_expr = search.SortExpression(expression=location_sort_expr,
                                    direction=search.SortExpression.ASCENDING,
                                    default_value=default_distance)
  distance_sort = search.SortOptions(expressions=[sort_expr])
  query = search.Query(query_string=query_string,
                       options=search.QueryOptions(
                        limit=result_limit,
                        sort_options=distance_sort))
  return _do_proximity_query(query)


def get_document_for_scene(scene_id):
  return search.Index(name=INDEX_NAME).get(scene_id)


def create_document_for_scene(scene_id):
  scene_data = placedlit.PlacedLit.get_place_from_id(scene_id)
  geopoint = search.GeoPoint(scene_data.location.lat, scene_data.location.lon)
  return search.Document(
    doc_id=unicode(scene_id),
    fields=[
      search.TextField(name='title', value=scene_data.title),
      search.TextField(name='author', value=scene_data.author),
      search.GeoField(name='scene_location', value=geopoint),
      search.DateField(name='date_added', value=scene_data.ts)
    ]
  )


def update_scene_index(scene_id):
  document = create_document_for_scene(scene_id)
  try:
    index = search.Index(name=INDEX_NAME)
    index.put(document)
  except search.Error:
    logging.info('put failed')
    raise


def batch_update_all_scenes(cursor=None, num_updated=0):
  query = placedlit.PlacedLit.all()
  if cursor:
    query.with_cursor(cursor)

  to_put = list()
  for place in query.fetch(limit=BATCH_SIZE):
    scene_id = place.key().id()
    document = create_document_for_scene(scene_id)
    to_put.append(document)

  if to_put:
    try:
      index = search.Index(name=INDEX_NAME)
      index.put(to_put)
      num_updated += len(to_put)
      logging.debug(
        'Put %d documents to index for a total of %d', len(to_put), num_updated)
      deferred.defer(
        batch_update_all_scenes, cursor=query.cursor(), num_updated=num_updated)
    except search.Error:
      logging.info('put failed')
      raise
