import unittest

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed


class TestModel(db.Model):
  pass


class TestEntityGroupRoot(db.Model):
  """Entity group root"""
  pass


def GetEntityViaMemcache(entity_key):
  """Get entity from memcache if available, from datastore if not."""
  entity = memcache.get(entity_key)
  if entity is not None:
    return entity
  entity = TestModel.get(entity_key)
  if entity is not None:
    memcache.set(entity_key, entity)
  return entity


class HomepageTestCase(unittest.TestCase):

  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def test_root_url_resolves_to_home_page_view(self):
    # found = resolve('/')
    # self.assertEqual(found.func, home_page)
    pass

  def test_home_page_returns_correct_html(self):
    # request = HttpRequest()
    # response = home_page(request)
    # expected_html = render_to_string('home.html')
    # self.assertEqual(response.content, expected_html)
    pass

if __name__ == '__main__':
  unittest.main()
