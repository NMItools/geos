import psycopg2

# verzija
ver = 2.0

# =============================================================
# definisanje globalnih varijabli:

# osnovni URL za ortofoto
of_base_url = "https://a3.geosrbija.rs/proxies/xWmsProxy.ashx?"

# osnovni URL za Katastar Nepokretnosti:
kn_base_url = "https://ogc.geosrbija.rs/mapserv.ashx?"

# folder gde se skidaju preuzete PNG slike:
dl_path = r"D:/geosrbija/"

# PostGIS konekcija - kućni server vs jkp "Naissus"
# server = 'localhost'
server = 'VERDI'
baza = 'geosrbija'
user = 'postgres'
password = 'softdesk'
table_name = 'gs_bbox_grid'

connection = psycopg2.connect(
    dbname=baza,
    user=user,
    host=server,
    password=password
    )
cursor = connection.cursor()

# ostalo
header = None
uuid = None
keys = None
dX = None
dY = None
dW = None
dH = None
