import json

from google.appengine.ext import webapp

from handlers.abstracts import baseapp
from classes import placedlit


class PlaceHandler(baseapp.BaseAppHandler):
  def get(self, id):
    pl = placedlit.PlacedLit.get_place_from_id(id)
    place_info = {
        'title': pl.title,
        'author': pl.author,
        'place_name': pl.scenelocation,
        'description': pl.scenedescription,
        'notes': pl.notes,
        'date_added': pl.ts.strftime('%m-%d-%Y'),
        'visits': pl.checkins,
        'lat': pl.location.lat,
        'lon': pl.location.lon
        }
    self.output_json(json.dumps(place_info))

urls = [
  ('/place/(.*)', PlaceHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
