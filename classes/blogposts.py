"""
Blog posts are pulled from Wordpress RSS.
Using the publication date to determine uniqueness. (I know.)
Before creating a post, publication timestamp is check to prevent duplicates.
"""
# pylint: disable=R0904

from datetime import datetime

from google.appengine.ext import db


DEFAULT_LIMIT = 7


class Blogpost(db.Expando):
  """ Represents a blog post """
  title = db.StringProperty()
  link = db.StringProperty()
  pub_date = db.DateTimeProperty()
  description = db.TextProperty()

  @classmethod
  def create_from_dict(cls, blog_data):
    """ new blog post from dict. returns new key or existing key. """
    pub_date = datetime.strptime(blog_data['pub_date'],
                                 '%a, %d %b %Y %H:%M:%S +0000')
    try:
      keys = [post.key for post in Blogpost.get_post_by_pub_date(pub_date)]
      return keys[0]
    except IndexError:
      post = cls(
        title=blog_data['title'],
        link=blog_data['link'],
        description=blog_data['description'],
        pub_date=pub_date)
      post.put()
      return post.key()

  @classmethod
  def get_newest_posts(cls, limit=DEFAULT_LIMIT):
    """ we only want to show newest posts """
    post_query = Blogpost.all()
    post_query.order('-pub_date')
    return post_query.run(limit=limit)

  @classmethod
  def get_post_by_pub_date(cls, pub_date):
    """ this should return nothing if no post with a matching date exists """
    query = Blogpost.all().filter('pub_date =', pub_date)
    return query.run()
