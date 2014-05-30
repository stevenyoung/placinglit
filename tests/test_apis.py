import unittest
import logging

# from google.appengine.api import memcache
# from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.api import app_identity


class AppIdentityTestCase(unittest.TestCase):

  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    # self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    self.testbed.init_app_identity_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def test_app_identity_api_returns_testbed_id(self):
    app_id = app_identity.get_application_id()
    self.assertEqual(app_id, 'testbed-test')

  def test_app_identity_api_returns_access_token(self):
    access_token = app_identity.get_access_token('user@here.com')
    self.assertEqual(access_token, 'open sesame')

  def test_app_identity_api_returns_default_hostname(self):
    hostname = app_identity.get_default_version_hostname()
    self.assertEqual(hostname, 'open sesame')

  def test_app_identity_api_returns_service_account_name(self):
    hostname = app_identity.get_service_account_name()
    self.assertEqual(hostname, 'test@localhost')

if __name__ == '__main__':
  unittest.main()
