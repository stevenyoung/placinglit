"""
handlers.place

Created on Dec 19, 2012
"""

__author__ = 'steven@eyeballschool.com (Steven)'


import json

from string import capwords

from google.appengine.ext import webapp
from google.appengine.api import users

from handlers.abstracts import baseapp
from classes import placedlit
from classes import user_request


class AddPlacesHandler(baseapp.BaseAppHandler):
  def post(self):
    place_data = json.loads(self.request.body)
    place_data['user'] = users.get_current_user()
    place_key = placedlit.PlacedLit.create_or_update_from_dict(place_data)

    agent = self.request.headers['User-Agent']
    user_request.UserRequest.create(ua=agent, user_loc=place_key)

    response_message = '%s by %s added at <br>location: (%s, %s)<br>thanks.' % (
      place_data['title'], place_data['author'], place_data['latitude'],
      place_data['longitude'])
    response_json = {
      'message': response_message,
      'geopt': { 'lat': place_data['latitude'], 'lng': place_data['longitude']}
    }

    self.output_json(response_json)


class GetPlacesHandler(baseapp.BaseAppHandler):
  def get(self):
    places = placedlit.PlacedLit.get_all_places()
    loc_json = []
    for place in places:
      geo_pt = place.location
      key = place.key()
      loc = {
        'latitude': geo_pt.lat,
        'longitude': geo_pt.lon,
        'title': place.title,
        'author': place.author,
        'db_key': key.id()}
      loc_json.append(loc)
    self.output_json(loc_json)


class RecentPlacesHandler(baseapp.BaseAppHandler):
  def get(self):
    places = placedlit.PlacedLit.get_newest_places(limit=10)
    loc_json = []
    for place in places:
      date_added = place.ts.strftime('%m-%d-%Y')
      geo_pt = place.location
      key = place.key()
      loc = {
        'latitude': geo_pt.lat,
        'longitude': geo_pt.lon,
        'title': place.title,
        'author': place.author,
        'date_added': date_added,
        'db_key': key.id()}
      if place.scenelocation:
        loc['location'] = capwords(place.scenelocation)
      loc_json.append(loc)
    self.output_json(loc_json)


class InfoHandler(baseapp.BaseAppHandler):
  def get(self, place_id):
    place = placedlit.PlacedLit.get_place_from_id(place_id)
    if place:
      date_added = place.ts.strftime('%m-%d-%Y')
      place_info = {
        'id': place_id,
        'title': place.title,
        'author': place.author,
        'place_name': place.scenelocation,
        'scenetime': place.scenetime,
        'actors': place.actors,
        'symbols': place.symbols,
        'description': place.scenedescription,
        'notes': place.notes,
        'date_added': date_added,
        'visits': place.checkins,
      }
      if place.image_url:
        place_info['image'] = place.image_url.replace('http://', '')
      self.output_json(place_info)


class ExportPlacesHandler(baseapp.BaseAppHandler):
  def get(self):
    places = placedlit.PlacedLit.get_all_places()
    row_id = 1
    loc_csv = '"id","title","author","location","time","actors","symbols",'
    loc_csv += '"description","notes","latitude","longitude"\n'
    for place in places:
      geo_pt = place.location
      loc_csv += '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(
        row_id, place.title, place.author, place.scenelocation, place.scenetime,
        place.actors, place.symbols, place.scenedescription, place.notes,
        geo_pt.lat, geo_pt.lon, place.ts)
      row_id += 1
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.out.write(loc_csv)


class PlacesVisitHandler(baseapp.BaseAppHandler):
  def get(self, place_id):
    place = placedlit.PlacedLit.get_place_from_id(place_id)
    place.update_visit_count()
    info_path = '/places/info/' + place_id
    self.redirect(info_path)


class CountPlacesHandler(baseapp.BaseAppHandler):
  def get(self):
    count_data = {
      'count': placedlit.PlacedLit.count()
    }
    self.output_json(count_data)


urls = [
  ('/places/add', AddPlacesHandler),
  ('/places/show', GetPlacesHandler),
  ('/places/info/(.*)', InfoHandler),
  ('/places/visit/(.*)', PlacesVisitHandler),
  ('/places/recent', RecentPlacesHandler),
  ('/places/export', ExportPlacesHandler),
  ('/places/count', CountPlacesHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
