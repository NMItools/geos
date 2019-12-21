import unittest
from gswms import GeoSrbijaWMS


class TestGeoSrbijaWMS(unittest.TestCase):
    """ Test metoda GeoSrbijaWMS klase:
        - URL (http)
        - header (http)
        - tip (kn ili of)
        - ime (originalno ime sloja na sajtu)
        - path (putanja za download folder)
        - filename (generisano ime za preuzeti fajl)
    """

    def setUp(self):
        self.gswms = GeoSrbijaWMS('parcele', 569000, 4790500)

    def test_url_generation_method(self):
        url_test = (
                    "https://ogc.geosrbija.rs/mapserv.ashx?"
                    "LAYERS=layer_532&QUERYABLE=false&TRANSITIONEFFECT=resize&"
                    "TRANSPARENT=TRUE&INFOFORMAT=text%2Fhtml&"
                    "FORMAT=image%2Fpng&VERSION=1.3.0&EXCEPTIONS=XML&GUI=8"
                    "&A3TKN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoib"
                    "WFwc2VydmVyIiwibmJmIjoxNTcxMDQ0NTA1LCJleHAiOjE1NzEzOTAx"
                    "MDUsImlhdCI6MTU3MTA0NDUwNX0.kmzjR5sLGe47rSUJgqPuZ5_"
                    "ZK2wwx1eEfgePIkntwGE&"
                    "SERVICE=WMS&REQUEST=GetMap&STYLES=&CRS=EPSG%3A32634"
                    "&BBOX=569000,4790500,569500,4791000&WIDTH=3000&"
                    "HEIGHT=3000"
                    )
        self.assertEqual(url_test, self.gswms.url)

    def test_header_method(self):
        header_test = {'Accept': 'image/webp,*/*', 
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Connection': 'keep-alive',
                       'Cookie': '_ga=GA1.2.122374505.1511963246; _gid=GA1.2.722972071.1571044509',
                       'DNT': '1', 'Host': 'ogc.geosrbija.rs', 'Referer': 'https://a3.geosrbija.rs/',
                       'TE': 'Trailers',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
        self.assertEqual(header_test, self.gswms.header)

    def test_tip_method(self):
        self.assertEqual('kn', self.gswms.tip)

    def test_ime_method(self):
        self.assertEqual('layer_532', self.gswms.gs_ime)

    def test_path_generation_method(self):
        self.assertEqual('D:/geosrbija/kn/parcele/PNG/', self.gswms.path)

    def test_filename_generation_method(self):
        self.assertEqual('parcele_569000_4790500', self.gswms.filename)


if __name__ == '__main__':
    unittest.main()
