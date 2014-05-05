"""
handlers.home description.

Created on Nov 19, 2012
"""

__author__ = 'steven@eyeballschool.com (Steven)'

import json
import logging

from google.appengine.ext import webapp

from handlers.abstracts import baseapp
from classes import placedlit
import blogposts
import urlparse


class HomeHandler(baseapp.BaseAppHandler):
  def get(self):
    template_values = self.basic_template_content()
    template_values['title'] = 'Home'
    posts = blogposts.BlogpostsHandler.posts_for_display()
    bloglinks = [{'title': post.title, 'link': post.link} for post in posts]
    template_values['posts'] = bloglinks
    self.render_template('home.tmpl', template_values)


class AboutHandler(baseapp.BaseAppHandler):
  def get(self):
    template_values = self.basic_template_content()
    template_values['title'] = 'About'
    self.render_template('about.tmpl', template_values)


class FundingHandler(baseapp.BaseAppHandler):
  def get(self):
    template_values = self.basic_template_content()
    template_values['title'] = 'Funding'
    self.render_template('funding.tmpl', template_values)


class MapHandler(baseapp.BaseAppHandler):
  def get(self, location=None, key=None):
    key = self.request.get('key')
    template_values = self.basic_template_content()
    template_values['title'] = 'Map'
    if location:
      if ',' in location:
        (lat, lng) = location.replace('/', '').split(',')
        template_values['center'] = '{lat:%s,lng:%s}' % (lat, lng)
    if key:
      template_values['key'] = key

    # FIXIT: pass all scenes to template for map markers
    # places = placedlit.PlacedLit.get_all_places()
    # loc_json = [self.export_place_fields(place) for place in places]
    # template_values['scenes'] = json.dumps(loc_json)

    self.render_template('map.tmpl', template_values)


class UserstatusHandler(baseapp.BaseAppHandler):
  def get(self):
    return self.get_user_status()


class AllscenesHandler(baseapp.BaseAppHandler):
  def get(self):
    template_values = self.basic_template_content()
    template_values['title'] = 'All Scenes'
    self.render_template('all.tmpl', template_values)


class AdminEditSceneHandler(baseapp.BaseAppHandler):
  def get(self):
    template_values = self.basic_template_content()
    template_values['title'] = 'Edit Scene'
    place_id = self.request.get('key')
    logging.info('edit %s', place_id)
    place = placedlit.PlacedLit.get_place_from_id(place_id)
    logging.info('place %s', place)
    template_values['place'] = place
    self.render_template('edit.tmpl', template_values)

  def post(self):
    """ add scene from user submission """
    logging.info('place_id: %s', self.request.get('key'))
    logging.info('edit scene: %s', self.request.body)
    logging.info('title: %s', self.request.get('title'))
    place = placedlit.PlacedLit.get_place_from_id(self.request.get('key'))
    logging.info('place: %s', place)
    if place:
      place.title = self.request.get('title')
      place.author = self.request.get('author')
      place.actors = self.request.get('actors')
      place.notes = self.request.get('notes')
      place.scenedescription = self.request.get('description')
      place.scenelocation = self.request.get('place_name')
      place.scenetime = self.request.get('scenetime')
      place.symbols = self.request.get('symbols')
      place.ug_isbn = self.request.get('ug_isbn')

      if place.image_url:
        image_url = urlparse.urlsplit(place.image_url)
        if image_url.scheme and image_url.netloc:
          place.image_url = urlparse.urlunsplit(image_url)

      place.put()


class NewhomeHandler(baseapp.BaseAppHandler):
  def get(self):
    template_values = self.basic_template_content()
    template_values['title'] = 'Home'
    posts = blogposts.BlogpostsHandler.posts_for_display()
    bloglinks = [{'title': post.title, 'link': post.link} for post in posts]
    template_values['posts'] = bloglinks
    self.render_template('placinglit.tmpl', template_values)


class MapFilterHandler(baseapp.BaseAppHandler):
  def get(self, field=None, term=None):
    template_values = self.basic_template_content()
    template_values['title'] = 'Map'
    places = placedlit.PlacedLit.places_by_query(field, term)
    loc_json = []
    if places:
      loc_json = [self.export_place_fields(place) for place in places]
    template_values['scenes'] = json.dumps(loc_json)
    self.render_template('map.tmpl', template_values)


urls = [
  ('/about', AboutHandler),
  ('/all', AllscenesHandler),
  ('/funding', FundingHandler),
  ('/home', HomeHandler),
  ('/map/filter/(.*)/(.*)', MapFilterHandler),
  ('/map(/?.*)', MapHandler),
  ('/', HomeHandler),
  ('/user/status', UserstatusHandler),
  ('/top/', NewhomeHandler),
  ('/admin/edit', AdminEditSceneHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
