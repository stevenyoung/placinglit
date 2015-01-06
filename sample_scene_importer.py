#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" import sample scenes """

import json
import unicodedata
import urllib
import urllib2

DEST_JSON = 'http://localhost:9999/places/import'


def retrieve_json_from_file(source=None):
  """ scenes from json on disk """
  with open(source, 'r') as dump:
    jsondump = json.loads(dump.read())
  return jsondump


def insert_from_file(data, import_url=DEST_JSON, limit=None):
  """ insert scenes from json on disk """
  print 'length %d' % (len(data))
  count = 0
  import_data = data
  if limit:
    import_data = import_data[-limit:]
  for place_record in import_data:
    try:
      place_data = urllib.urlencode(place_record)
      urllib2.urlopen(urllib2.Request(import_url, place_data))
      count += 1
    except UnicodeEncodeError:
      pass
    print count


def main():
  """ do it """
  insert_from_file(retrieve_json_from_file(source='sample_data.json'))

if __name__ == '__main__':
  main()
