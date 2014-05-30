import logging

import xml.etree.ElementTree as et

from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from handlers.abstracts import baseapp
from classes import blogposts


POST_COUNT = 7  # number of posts to display
BLOG_FEED_URL = 'http://placingliterature.wordpress.com/feed/'


class BlogpostsHandler(baseapp.BaseAppHandler):
  def get(self):
    fetch_headers = {'Cache-Control': 'no-cache,max-age=300',
                     'Pragma': 'no-cache'}
    result = urlfetch.fetch(BLOG_FEED_URL, None, urlfetch.GET, fetch_headers)
    logging.info(str(result.status_code) + ' ' + str(result.headers))
    poststring = str(result.content)
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

    links = alllinks[:POST_COUNT]
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
