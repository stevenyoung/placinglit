#!/usr/bin/env python

import json
import urllib
import urllib2

SOURCE_JSON = 'http://beta04.placingliterature.appspot.com/places/dump'
DEST_JSON = 'http://localhost:9999/places/import'


class PlacesImporter():
  def retrieve(self, export_source=SOURCE_JSON):
    jsondump = urllib2.urlopen(export_source).read()
    return jsondump

  def insert(self, data, import_url=DEST_JSON):
    import_data = json.loads(data)
    print('length %d' % (len(import_data)))
    count = 1
    for place_record in import_data:
      print count
      try:
        place_data = urllib.urlencode(place_record)
        print place_data
        urllib2.urlopen(urllib2.Request(import_url, place_data))
        count += 1
      except UnicodeEncodeError:
        pass


if __name__ == '__main__':
  importer = PlacesImporter()
  importer.insert(importer.retrieve())
