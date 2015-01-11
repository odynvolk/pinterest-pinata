import unittest
from pinata.client import PinterestPinata
import pdb


class TestClientSearches(unittest.TestCase):
    def setUp(self):
        self.pinata = PinterestPinata(email='whoever@whenever.com', password='youcanneverguessit', username='catlover')

    def test_boards(self):
        self.assertTrue(len(self.pinata.boards('david')) > 10)

    def test_search_boards(self):
        self.assertTrue(len(self.pinata.search_boards('cats')) > 15)

    def test_search_pins(self):
        self.assertTrue(len(self.pinata.search_pins('persian cats')) > 5)
