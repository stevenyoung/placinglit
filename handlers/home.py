"""
handlers.home description.

Created on Nov 19, 2012
"""

__author__ = 'steven@eyeballschool.com (Steven)'

import json
import logging

from google.appengine.ext import webapp

from classes import placedlit

from handlers.abstracts import baseapp

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
        # use scene index to select places
        places = placedlit.get_nearby_places(lat, lng)
        loc_json = []
        for doc in places:
          place_dict = {'db_key': doc.doc_id}
          for field in doc.fields:
            if field.name == 'scene_location':
              place_dict['latitude'] = field.value.latitude
              place_dict['longitude'] = field.value.longitude
            else:
              place_dict[field.name] = field.value
          loc_json.append(place_dict)
        if loc_json:
          template_values['scenes'] = json.dumps(loc_json)
    if key:
      template_values['key'] = key
    # FIXIT: pass all scenes to template for map markers
    # places = placedlit.PlacedLit.get_all_places()
    # loc_json = [self.export_place_fields(place) for place in places]

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
    place = placedlit.PlacedLit.get_place_from_id(place_id)
    template_values['place'] = place
    self.render_template('edit.tmpl', template_values)

  def post(self):
    """ add scene from user submission """
    place = placedlit.PlacedLit.get_place_from_id(self.request.get('key'))
    if place:
      place_data = dict()
      update_fields = ['title', 'author', 'scenelocation', 'scenedescription',
                       'notes', 'image_url', 'actors', 'scenetime', 'symbols',
                       'ug_isbn']
      for field in update_fields:
        place_data[field] = self.request.get(field)
      place.update_fields(place_data)
      self.response.out.write('Saved')

  def delete(self):
    logging.info('deleted %s', self.request.get('key'))
    place = placedlit.PlacedLit.get_place_from_id(self.request.get('key'))
    place.delete_scene()
    self.response.out.write('Deleted')


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


class AdminMenuHandler(baseapp.BaseAppHandler):
  def get(self):
    template_values = self.basic_template_content()
    template_values['title'] = 'Admin Menu'
    self.render_template('admin.tmpl', template_values)


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
  ('/admin/edit', AdminEditSceneHandler),
  ('/admin/menu', AdminMenuHandler),
]

app = webapp.WSGIApplication(urls, debug=True)
