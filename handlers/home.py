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


class NewhomeHandler(baseapp.BaseAppHandler):
  def get(self):
    template_values = self.basic_template_content()
    template_values['title'] = 'Home'
    posts = blogposts.BlogpostsHandler.posts_for_display()
    bloglinks = [{'title': post.title, 'link': post.link} for post in posts]
    template_values['posts'] = bloglinks
    self.render_template('home2.tmpl', template_values)


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
  ('/newhome', NewhomeHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
