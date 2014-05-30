""" Datastore model for scene location documents """

from google.appengine.ext import ndb


def reset_updates():
  ndb.delete_multi(StatusUpdate.query().fetch(keys_only=True))


class StatusUpdate(ndb.Model):
  status_text = ndb.StringProperty()
  timestamp = ndb.DateTimeProperty(auto_now_add=True)

  def add_update(self, status_text=None):
    reset_updates()
    self.status_text = status_text
    self.put()

  def is_duplicate_update(self, status_text=None):
    update_query = StatusUpdate.query(StatusUpdate.status_text == status_text)
    matching_updates = [result for result in update_query.iter()]
    if len(matching_updates) < 1:
      return False
    else:
      return True
