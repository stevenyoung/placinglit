import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    # self.browser = webdriver.Firefox()
    self.browser = webdriver.Chrome()

  def tearDown(self):
    self.browser.quit()

  def test_can_view_home_page_and_get_newest_content(self):
    # sweet app. lets check out the home page
    self.browser.get('http://localhost:9999')

    # TODO the page title needs updating
    self.assertIn('Home', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h3').text
    self.assertIn('Placing Literature', header_text)

    self.fail('Finish the test!')

  def test_can_view_map_page_and_add_new_title(self):
    # let's look at the mapped locations
    self.browser.get('http://localhost:9999/map')
    # would you like to add another item?
    # he types 'put stamp on envelope'.
    # he hits enter, page updates, now both items are in the list
    # will this list be here in the morning?
    # - there is a unique url according to the expository text
    # he visits that url. his list is still there.
    # now he can sleep.

    # user clicks a map to add an item and the marker appears?
    googlemap = self.browser.find_element_by_id('map_canvas')
    googlemap.click()

    #user
    inputbox = self.browser.find_element_by_id('title')
    self.assertIn('Book Title', inputbox.get_attribute('placeholder'))
    # he types 'find my postage stamps'.
    inputbox.send_keys('find my postage stamps')
    # he hits enter, page updates, 'postage stamps' are in the new list.
    inputbox.send_keys(Keys.ENTER)
    self.fail('Finish the test!')

    # table = self.browser.find_element_by_id('id_list_table')
    # rows = table.find_elements_by_tag_name('tr')
    # self.assertTrue(
    #   any(row.text == '1: find my postage stamps' for row in rows),
    #   'new to-do item did not appear in table'
    # )


if __name__ == '__main__':
  unittest.main()
