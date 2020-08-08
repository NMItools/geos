# verzija
verzija = 2.0

# =============================================================
# definisanje globalnih varijabli:

# folder gde se skidaju preuzete PNG slike:
dl_path = r"D:/geosrbija/"

gs_slojevi = {
    'sat_2010_10cm': ["Satelitski_snimci-30cm_2015-2016", "sat", 0],
    'sat_2013_10cm': ["Satelitski_snimci-40cm_2015-2016", "sat", 0],
    'of_2010_10cm': ["Orthophoto-10cm_(2007-2010)", "of", 0],
    'of_2013_10cm': ["Orthophoto-10cm_(2011-2013)", "of", 0],
    'of_2010_40cm': ["Orthophoto-40cm_(2007-2010)", "of", 0],
    'of_2013_40cm': ["Orthophoto-40cm_(2011-2013)", "of", 0],
    'parcele': ["layer_532", "kn", 1],  # 532 PARCELE (ISTOK)
    'parcele_jug': ["layer_533", "kn", 1],  # 533 PARCELE (JUG)
    'ulice':    ["layer_32", "kn", 1],  # ULICA
    'objekti': ["layer_280", "kn", 1],  # OBJEKAT
    'kbr':      ["layer_36", "kn", 1],  # KUĆNI BROJ
    'nazivi':   ["layer_54", "kn", 0],  # NAZIVI(DKP)
    'ko':       ["layer_61", "kn", 0],  # KATASTARSKA OPŠTINA
    'naselja':  ["layer_30", "kn", 0],  # NASELJE
    'sst':     ["layer_247", "kn", 0],  # Skupštine stanara
    'test':      ["layer_100", "kn", 0]   # test sloj
}

slojevi = [sloj for sloj in gs_slojevi]

# širina koordinatnog kvadrata u pixelima:
# ortofoto
# dw = 2048
# dh = 2048

# katastar
dw = 5120
dh = 5120

# širina koordinatnog kvadrata u m:
dx = 500
dy = 500

# osnovni HTTP parametri za ortofoto
of_base_url = "https://a3.geosrbija.rs/proxies/xWmsProxy.ashx?"

uuid = 'b90fb82a-483e-4eaf-8203-bfa89432c7de'
key = '20181025112412'

of_header = {'Accept': 'image/webp,*/*',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'en-US,en;q=0.5',
             'Connection': 'keep-alive',
             'Cookie': 'lng=sr; '
             'popup_b17ac663-2e23-425c-bc06-075e168997c1=974611082',
             'DNT': '1',
             'Host': 'a3.geosrbija.rs',
             'Referer': 'https://a3.geosrbija.rs/',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
             'Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
             }

# osnovni HTTP parametri za Katastar Nepokretnosti:
kn_base_url = "https://ogc.geosrbija.rs/mapserv.ashx?"

A3TKN = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoibWFwc2VydmVyIiwibmJmIjoxNTk2OTI2OTkyLCJleHAiOjE1OTcyNzI1OTIsImlhdCI6MTU5NjkyNjk5Mn0.97ktnvGgHySWwykv7aikwqXyCvouFKqG8Nnp4ZDLUCQ")

kn_header = {'Accept': 'image/webp,*/*',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'en-US,en;q=0.5',
             'Connection': 'keep-alive',
             'Cookie': '_ga=GA1.2.951720339.1596926996; _gid=GA1.2.137516005.1596926996; _gat=1',
             'DNT': '1',
             'Host': 'ogc.geosrbija.rs',
             'Referer': 'https://a3.geosrbija.rs/',
             'TE': 'Trailers',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; ' +
             'Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
             }