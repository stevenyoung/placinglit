import json

from google.appengine.ext import webapp
from google.appengine.api import users

from handlers.abstracts import baseapp

from classes import user_request
from classes import placedlit
from classes import site_users


def post_place_to_twitter(scene_key=None):
  """ update twitter status """
  import os
  # do not post to twitter if running on dev
  if not os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    scene_data = placedlit.PlacedLit.get_place_from_id(scene_key.id())
    from handlers import twitter
    from handlers.abstracts import keys
    oauth = twitter.OAuth(token=keys.tw_keys['OAUTH_TOKEN'],
                          token_secret=keys.tw_keys['OAUTH_TOKEN_SECRET'],
                          consumer_key=keys.tw_keys['CONSUMER_KEY'],
                          consumer_secret=keys.tw_keys['CONSUMER_SECRET'])
    t = twitter.Twitter(auth=oauth)
    status = "{} by {} was mapped on PlacingLiterature.com. #literaryroadtrip"
    update = status.format(scene_data.title, scene_data.author)
    t.statuses.update(status=update)


class AddPlacesHandler(baseapp.BaseAppHandler):
  """ adding a place from user interaction """
  def post(self):
    """ add scene from user submission """
    self.place_data = json.loads(self.request.body)
    self.place_data['user'] = users.get_current_user()
    self.place_data['email'] = users.get_current_user().email()
    place_key = placedlit.PlacedLit.create_from_dict(self.place_data)
    self.add_scene_to_user(scene_key=place_key)
    agent = self.request.headers['User-Agent']
    user_request.UserRequest.create(ua=agent, user_loc=place_key)
    self.send_response()
    post_place_to_twitter(scene_key=place_key)

  def add_scene_to_user(self, scene_key=None):
    """ update a users added and vistited scenes """
    user_email = self.place_data['email']
    if user_email:
      user = site_users.User.get_by_id(user_email)
      if not user:
        user = site_users.User.create(user_email)
      user.add_scene(scene_key)
      if self.place_data['check_in']:
        user.visit_scene(scene_key)

  def send_response(self):
    """ format user client response """
    scene_data = self.place_data
    response = '{} by {} added at <br>location: ({}, {})<br>thanks.'
    response_message = response.format(
      scene_data['title'], scene_data['author'],
      scene_data['latitude'], scene_data['longitude']
    )
    response_json = {
      'message': response_message,
      'geopt': {'lat': scene_data['latitude'], 'lng': scene_data['longitude']}
    }
    self.output_json(response_json)



urls = [
  ('/places/add', AddPlacesHandler),
]

app = webapp.WSGIApplication(urls, debug=True)
