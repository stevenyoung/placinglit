""" Datastore model for scene location documents """
import logging

from google.appengine.api import search

INDEX_NAME = 'StatusUpdate'


def matches_last_twitter_status_update(status):
  """ query search index for last twitter status update """
  query_string = 'status = \"{}\"'.format(status)
  doc_index = search.Index(name=INDEX_NAME)
  query = search.Query(query_string=query_string)
  results = doc_index.search(query)
  if len(results):
    return True
  else:
    return False


def set_last_twitter_status_update(status):
  """ store last twitter update in search index """
  empty_scene_index(index_name=INDEX_NAME)
  indexed_status = create_update_doc_for_status(status)
  try:
    index = search.Index(name=INDEX_NAME)
    index.put(indexed_status)
  except search.Error:
    logging.info('put failed')
    raise


def create_update_doc_for_status(status):
  """ search document for status updates """
  return search.Document(fields=[
    search.TextField(name='status', value=status)
    ]
  )


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
