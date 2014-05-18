import logging

from google.appengine.api import search

photo_index = search.Index(name='PanoramioIndex')


def add_scene_to_panoramio_index(scene_id, photo_id, owner_id):
  scene_id = str(scene_id)
  owner_id = str(owner_id)
  document = search.Document(
    # doc_id=photo_id,
    fields=[
      search.AtomField(name='scene_id', value=scene_id),
      search.AtomField(name='owner_id', value=owner_id),
    ])
  try:
    photo_index.put(document)
  except search.Error:
    logging.info('put failed')
    raise


def has_panoramio_photos(scene_id):
  query_string = 'scene_id = {}'.format(scene_id)
  return photo_index.search(query_string).number_found > 0


def empty_panoramio_index():
  """Delete all the docs in the given index."""
  logging.info('empty photo index')
  doc_index = photo_index

  # looping because get_range by default returns up to 100 documents at a time
  while True:
  # Get a list of documents populating only the doc_id field and extract the ids
    document_ids = [document.doc_id
                    for document in doc_index.get_range(ids_only=True)]
    if not document_ids:
      break
    # Delete the documents for the given ids from the Index.
    doc_index.delete(document_ids)


def index_info():
  logging.info('photo_index info')
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
