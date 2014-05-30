from datetime import datetime

from google.appengine.ext import db


class Blogpost(db.Expando):
  title = db.StringProperty()
  link = db.StringProperty()
  pub_date = db.DateTimeProperty()
  description = db.TextProperty()

  @classmethod
  def create(cls, blog_data):
    post = cls(
      title=blog_data['title'],
      link=blog_data['link'],
      description=blog_data['description'],
    )
    post.pub_date = datetime.strptime(blog_data['pub_date'],
                                      '%a, %d %b %Y %H:%M:%S +0000')
    try:
      keys = [post.key for post in Blogpost.get_post_by_pub_date(post.pub_date)]
      return keys[0]
    except IndexError:
      post.put()
      return post.key()

  @classmethod
  def get_newest_posts(cls, limit=7):
    post_query = Blogpost.all()
    post_query.order('-pub_date')
    return post_query.run(limit=limit)

  @classmethod
  def get_post_by_pub_date(cls, pub_date):
    q = Blogpost.all().filter('pub_date =', pub_date)
    return q.run()
