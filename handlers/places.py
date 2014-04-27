""" Request handlers for places. """
# pylint: disable=W0403, R0904, C0103


import datetime
import json
import logging

from string import capwords

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import memcache

from handlers.abstracts import baseapp
from classes import placedlit
from classes import user_request
from classes import site_users


class AddPlacesHandler(baseapp.BaseAppHandler):
  """ adding a place from user interaction """
  def __init__(self):
    self.place_data = None

  def post(self):
    """ add scene from user submission """
    self.place_data = json.loads(self.request.body)
    self.place_data['user'] = users.get_current_user()
    self.place_data['email'] = users.get_current_user().email()
    place_key = placedlit.PlacedLit.create_from_dict(self.place_data)
    self.add_scene_to_user(scene_key=place_key)
    agent = self.request.headers['User-Agent']
    user_request.UserRequest.create(ua=agent, user_loc=place_key)
    self.send_response()
    self.post_to_twitter()

  def add_scene_to_user(self, scene_key=None):
    """ update a users added and vistited scenes """
    user_email = self.place_data['email']
    if user_email:
      user = site_users.User.get_by_id(user_email)
      if not user:
        user = site_users.User.create(user_email)
      user.add_scene(scene_key)
      if self.place_data['check_in']:
        user.visit_scene(scene_key)

  def send_response(self):
    """ format user client response """
    scene_data = self.place_data
    response = '{} by {} added at <br>location: ({}, {})<br>thanks.'
    response_message = response.format(
      scene_data['title'], scene_data['author'],
      scene_data['latitude'], scene_data['longitude']
    )
    response_json = {
      'message': response_message,
      'geopt': {'lat': scene_data['latitude'], 'lng': scene_data['longitude']}
    }
    self.output_json(response_json)

  def post_to_twitter(self):
    """ update twitter status """
    pass


class GetPlacesHandler(baseapp.BaseAppHandler):
  """ get all places and return as list of json objects"""
  def get(self):
    places = placedlit.PlacedLit.get_all_places()
    loc_json = []
    for place in places:
      place_dict = {
        'latitude': place.location.lat,
        'longitude': place.location.lon,
        'db_key': place.key().id(),
        'title': place.title,
        'author': place.author
      }
      loc_json.append(place_dict)
    # loc_json = [self.export_place_fields(place) for place in places]
    self.output_json(loc_json)


class GetPlacesByDateHandler(baseapp.BaseAppHandler):
  """ get all places sorted by date return as list of json objects"""
  def get(self):
    count = placedlit.PlacedLit.count()
    places = placedlit.PlacedLit.get_newest_places(limit=count)
    stats = memcache.get_stats()
    logging.info('memcache stats: %s' % (stats))
    loc_json = [self.export_place_fields(place) for place in places]
    self.output_json(loc_json)


class RecentPlacesHandler(baseapp.BaseAppHandler):
  """ get newest 10 places sorted by date return as list of json objects"""
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
  """ get info about a scene by id. """
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
      if place.ug_isbn:
        place_info['isbn'] = place.ug_isbn
      elif place.book_data:
        place_info['isbn'] = place.book_data.isbn13
      if place.image_url:
        place_info['image'] = place.image_url.replace('http://', '')
      self.output_json(place_info)


class ExportPlacesHandler(baseapp.BaseAppHandler):
  """ get places for csv export """
  def get(self):
    places = placedlit.PlacedLit.get_all_places()
    row_id = 1
    loc_csv = '"id","title","author","latitude","longitude","email"\n'
    fields = '"{}","{}","{}","{}","{}","{}"\n'
    for place in places:
      geo_pt = place.location
      try:
        loc_csv += fields.format(
          row_id, place.title, place.author,
          geo_pt.lat, geo_pt.lon, place.user_email)
        row_id += 1
      except UnicodeEncodeError:
        pass
    filename = 'filename="placingliterature_export_'
    filename += datetime.date.today().isoformat() + '.csv"'
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-Disposition'] = 'attachment; ' + filename
    self.response.out.write(loc_csv)


class PlacesVisitHandler(baseapp.BaseAppHandler):
  """ update visit count for a place. """
  def get(self, place_id):
    user_email = users.get_current_user().email()
    place = placedlit.PlacedLit.get_place_from_id(place_id)
    place.update_visit_count(user_email)
    info_path = '/places/info/' + place_id
    self.redirect(info_path)


class CountPlacesHandler(baseapp.BaseAppHandler):
  """ get a count of places added."""
  def get(self):
    count_data = {
      'count': placedlit.PlacedLit.count()
    }
    self.output_json(count_data)


class PlacesAuthors(baseapp.BaseAppHandler):
  """ get authors."""
  def get(self):
    author_places = placedlit.PlacedLit.get_all_authors()
    author_json = []
    for places in author_places:
      author_json.append({'author': places.author})
    self.output_json(author_json)


class PlacesTitles(baseapp.BaseAppHandler):
  """ get titles. """
  def get(self):
    title_places = placedlit.PlacedLit.get_all_titles()
    title_json = []
    for places in title_places:
      title_json.append({'title': places.title.replace('\"', '')})
    self.output_json(title_json)


urls = [
  ('/places/add', AddPlacesHandler),
  ('/places/show', GetPlacesHandler),
  ('/places/info/(.*)', InfoHandler),
  ('/places/visit/(.*)', PlacesVisitHandler),
  ('/places/recent', RecentPlacesHandler),
  ('/places/export', ExportPlacesHandler),
  ('/places/count', CountPlacesHandler),
  ('/places/authors', PlacesAuthors),
  ('/places/titles', PlacesTitles),
  ('/places/allbydate', GetPlacesByDateHandler),
]

app = webapp.WSGIApplication(urls, debug=True)
