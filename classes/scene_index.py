""" Datastore model for scene documents """
# pylint: disable=W0403, R0904, C0103

import logging

# from datetime import datetime
from google.appengine.api import search

import placedlit


def update_scene_index(scene_id):
  scene_data = placedlit.PlacedLit.get_place_from_id(scene_id)
  geopoint = search.GeoPoint(scene_data.location.lat, scene_data.location.lon)

  document = search.Document(
    doc_id=unicode(scene_id),
    fields=[
      search.TextField(name='title', value=scene_data.author),
      search.TextField(name='author', value=scene_data.author),
      search.GeoField(name='scene_location', value=geopoint)
    ]
  )

  try:
    index = search.Index(name="SceneIndex")
    index.put(document)
  except search.Error:
    logging.info('put failed')
    raise


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


def delete_all_in_index(index_name):
  """Delete all the docs in the given index."""
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


def location_query(lat, lon):
  distance = 1000000
  index = search.Index(name="SceneIndex")
  query_format = 'distance(scene_location, geopoint({}, {})) < {}'
  query_string = query_format.format(lat, lon, distance)
  logging.info('location query %s', query_string)
  try:
    results = index.search(query_string)
    total_matches = results.number_found
    number_of_docs_returned = len(results.results)
    logging.info('%s locations found', results.number_found)
    logging.info('%s total matches found', total_matches)
    logging.info('%s docs returned', number_of_docs_returned)
    return results.results
  except search.Error:
    logging.exception('Search failed')
