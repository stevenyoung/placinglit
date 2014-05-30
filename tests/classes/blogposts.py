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
      title = blog_data['title'],
      link = blog_data['link'],
      description = blog_data['description'],
    )
    post.pub_date = datetime.strptime(blog_data['pub_date'],
      '%a, %d %b %Y %H:%M:%S +0000' )
    post.put()
    return post.key()

  @classmethod
  def get_newest_posts(cls, limit=5):
    post_query = Blogpost.all()
    post_query.order('-pub_date')
    return post_query.run(limit=limit)
