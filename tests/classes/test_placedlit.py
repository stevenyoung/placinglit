import unittest

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from classes import placedlit


class TestModel(placedlit.PlacedLit):
  pass


class TestEntityGroupRoot(db.Expando):
  """Entity group root"""
  pass


def GetEntityViaMemcache(entity_key):
  """Get entity from memcache if available, from datastore if not."""
  entity = memcache.get(entity_key)
  print('\ngot {0} from memcache'.format(entity))
  if entity is not None:
    return entity
  entity = TestModel.get(entity_key)
  print('\ngot {0} from Model.get'.format(entity))
  if entity is not None:
    memcache.set(entity_key, entity)
  return entity


class PlacedlitTestCase(unittest.TestCase):
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

  def test_insert_entity(self):
    TestModel().put()
    self.assertEqual(1, len(TestModel.all().fetch(2)))

  def test_filter_by_number(self):
    root = TestEntityGroupRoot(key_name="root")
    TestModel(parent=root.key()).put()
    TestModel(number=17, parent=root.key()).put()
    query = TestModel.all().ancestor(root.key()).filter('number =', 42)
    results = query.fetch(2)
    self.assertEqual(1, len(results))
    self.assertEqual(42, results[0].number)

  def test_retrieve_entity(self):
    entity_key = str(TestModel(number=18).put())
    print('\nkey {0}'.format(entity_key))
    retrieved_entity = TestModel.get(entity_key)
    print('\nretrieved {entity_key}'.format(entity_key=str(retrieved_entity)))
    self.assertNotEqual(None, retrieved_entity)
    self.assertEqual(18, retrieved_entity.number)

  def test_get_entity_via_memcache(self):
    entity_key = str(TestModel(number=18).put())
    print('\nkey {0}'.format(entity_key))
    retrieved_entity = GetEntityViaMemcache(entity_key)
    print('\nretrieved {entity_key}'.format(entity_key=str(retrieved_entity)))
    self.assertNotEqual(None, retrieved_entity)
    self.assertEqual(18, retrieved_entity.number)
