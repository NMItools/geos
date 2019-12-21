import unittest
from gswms import GeoSrbijaWMS


class TestGeoSrbijaWMS(unittest.TestCase):

    def setUp(self):
        self.gswms = GeoSrbijaWMS()

    def test_url_generation_method(self):
        self.assertEqual(1, self.gswms.url())


if __name__ == '__main__':
    unittest.main()