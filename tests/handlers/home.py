"""
handlers.home description.

Created on Nov 19, 2012
"""

__author__ = 'steven@eyeballschool.com (Steven)'


from google.appengine.ext import webapp

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
    self.render_template('map.tmpl', template_values)


class UserstatusHandler(baseapp.BaseAppHandler):
  def get(self):
    return self.get_user_status()

urls = [
  ('/home', HomeHandler),
  ('/map(/?.*)', MapHandler),
  ('/', HomeHandler),
  ('/user/status', UserstatusHandler)
]

app = webapp.WSGIApplication(urls, debug=True)
