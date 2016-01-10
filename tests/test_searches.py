import unittest
import vcr
from pinata.client import PinterestPinata
import pdb

class TestClientSearches(unittest.TestCase):
    def setUp(self):
        self.pinata = PinterestPinata(email='whoever@whenever.com', password='youcanneverguessit', username='catlover')

    @vcr.use_cassette('fixtures/vcr_cassettes/boards.yaml', record_mode='new_episodes')
    def test_boards(self):
        self.assertTrue(len(self.pinata.boards('david')) > 10)

    @vcr.use_cassette('fixtures/vcr_cassettes/search_boards.yaml', record_mode='new_episodes')
    def test_search_boards(self):
        self.assertTrue(len(self.pinata.search_boards('cats')) > 15)

    @vcr.use_cassette('fixtures/vcr_cassettes/search_pins.yaml', record_mode='new_episodes')
    def test_search_pins(self):
        self.assertTrue(len(self.pinata.search_pins('persian cats')) > 5)
