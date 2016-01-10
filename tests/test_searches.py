import unittest
import vcr
from pinata.client import PinterestPinata
import pdb

class TestClientSearches(unittest.TestCase):
    def setUp(self):
        self.pinata = PinterestPinata(email='whoever@whenever.com', password='youcanneverguessit', username='catlover')

    @vcr.use_cassette('fixtures/vcr_cassettes/boards.yaml', record_mode='new_episodes')
    def test_boards(self):
        boards = self.pinata.boards('david')
        self.assertTrue(len(boards) > 10)
        self.assertEqual(boards[0]['id'], '111042015751340934')
        self.assertEqual(boards[10]['id'],  '70509619105017041')

    @vcr.use_cassette('fixtures/vcr_cassettes/search_boards.yaml', record_mode='new_episodes')
    def test_search_boards(self):
        boards = self.pinata.search_boards('cats')
        self.assertTrue(len(boards) > 15)
        self.assertEqual(boards[0]['id'], '108508740961118549')
        self.assertEqual(boards[10]['id'],  '562598247139642475')

    @vcr.use_cassette('fixtures/vcr_cassettes/search_pins.yaml', record_mode='new_episodes')
    def test_search_pins(self):
        pins = self.pinata.search_pins('persian cats')
        self.assertTrue(len(pins) > 20)
        self.assertEqual(pins[0]['id'], '456200637234822717')
        self.assertEqual(pins[0]['link'], u'http://www.ourfurryfriendz.info/search/label/Top%207%20Most%20Affectionate%20Cat%20Breeds')
        self.assertEqual(pins[10]['id'], '376121006355425841')
        self.assertEqual(pins[10]['link'], u'http://instagram.com/p/ygKPwMRbas/')
