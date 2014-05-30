import logging
import urllib2

import xml.etree.ElementTree as et

from google.appengine.ext import webapp

from handlers.abstracts import baseapp
from classes import blogposts

class BlogpostsHandler(baseapp.BaseAppHandler):
  def get(self):
    url = 'http://placingliterature.wordpress.com/feed/'
    wpfeed = urllib2.urlopen('http://placingliterature.wordpress.com/feed/')
    posts = wpfeed.read()
    wpfeed.close()
    poststring = str(posts)
    posts = et.fromstring(poststring)
    link_format = '<a href="{}">{}</a><br/>'
    alllinks = []
    for item in posts.iter('item'):
      item_title = item.find('title').text
      item_link = item.find('link').text
      item_pub_date = item.find('pubDate').text
      item_description = item.find('description').text
      bloglink = link_format.format(item_link, item_title)
      alllinks.append(bloglink)
      blog_data = {'title': item_title, 'link': item_link,
        'pub_date': item_pub_date, 'description': item_description}
      blogposts.Blogpost.create(blog_data)

    links = alllinks[:5]
    for link in links:
      self.response.out.write(link)

  @staticmethod
  def posts_for_display():
    posts = blogposts.Blogpost.get_newest_posts()
    return posts

  @staticmethod
  def get_newest_post():
    posts = blogposts.Blogpost.description()
    return posts[:1]

urls = [
  ('/blog/update', BlogpostsHandler),
]


app = webapp.WSGIApplication(urls, debug="True")