"""
===============================================================================
Preuzimanje podloga sa GeoSrbija portala na osnovu MREŽE KVADRATA u PostGIS
https://a3.geosrbija.rs
-------------------------------------------------------------------------------

    verzija:  3.2
    datum:    2019-AVGUST-11
    autor: Nebojša Pešić, dipl. građ. ing (nmiTools@gmail.com)

 preduslovi:
    Python 3.x (scoop reset python)
    pip install psycopg2
    pip install requests
    pip install clint
    pip install M:/MEGAsync/Python/whl/GDAL-3.0.1-cp37-cp37m-win_amd64.whl

===============================================================================
"""

import os
import os.path
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from clint.textui import progress
import psycopg2
from psycopg2 import sql
import osgeo.gdal as gdal

os.system('cls')

"""
 =============================================================================
 - SLOJEVI ZA PREUZIMANJE (Ortofoto i Katastar nepokretnosti)
 =============================================================================

 Radi lakšeg upravljanja preuzetih podloga definišemo oblast u kojoj je
 moguće vršiti preuzimanje. Teritorija/oblast je podeljena na mrežu kvadrata
 gde max dužina i visina jednog kvadrata (dX i dY u metrima) zavisi od toga
 koja se vrsta sloja preuzima (KATASTAR ili ORTOFOTO) tj. zbog postavljenih
 ograničenja na WMS serveru portala:

"""

# -----------------------------------------------------------------------------
# - Ortofoto (10cm i 40cm)
# -----------------------------------------------------------------------------
# Max dozvoljena širina/visina slike:
# 4096 pixela (ograničenje WMS servera)

# Stavljamo duplo manju vrednost jer server ima problema da izgeneriše
# maksimalnu sliku (~45 MB) i često ne uspeva da obradi zahtev.

# dW = 2048
# dH = 2048

# Max dimenzija po X/Y osi:             500 metara
# (najveće dozvoljeno uvećanje/ZOOM;  1 pixel = 0.1220703125 metara)

# dXof = 500
# dYof = 500

# -----------------------------------------------------------------------------
# - Katastar nepokretnosti
# -----------------------------------------------------------------------------
# Max dozvoljena širina/visina slike:
# 6000 pixela (ograničenje WMS servera)

# dW = 6000
# dH = 6000

# Max dimenzija po X/Y osi:             1000 metara
# (najveće dozvoljeno uvećanje/ZOOM;  1 pixel = 0.16 metara)
# dX = 500
# dY = 500

print("----------------------------------------------------------------------")

# osnovni URL za ortofoto
of_base_url = "https://a3.geosrbija.rs/proxies/xWmsProxy.ashx?"

# osnovni URL za Katastar Nepokretnosti:
kn_base_url = "https://ogc.geosrbija.rs/mapserv.ashx?"

# folder gde se skidaju preuzete PNG slike:
dl_path = r"D:/geosrbija/"


# =============================================================================
# PostGIS konekcija - za pristup MREŽI KVADRATA u PostGIS tabeli "gs_bbox_grid"
# =============================================================================
# kućni server vs. jkp "Naissus"

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
    password=password)

cursor = connection.cursor()

# =============================================================================
# - Potrebne funkcije za rad
# =============================================================================


# ponavljanje neuspešnih HTTP zahteva
def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


# kreiranje WLD/PGW fajla za georeferencu rastera
def wld_file(imgfilename, bbox_l):
    wld = open(imgfilename + '.pgw', 'w')
    wld.write(str(dX/dW)+"\n")
    wld.write("0.00000000\n")
    wld.write("0.00000000\n")
    wld.write(str(-(dY/dH))+"\n")
    wld.write(str(bbox_l[0])+"\n")
    wld.write(str(bbox_l[3])+"\n")
    wld.close()


# kreiranje MapInfo TAB fajla za georeferencu rastera
def generate_mitab(imgfilename, bbox_l):
    src = gdal.Open(imgfilename)
    dx_pix = (dX/dW)/2
    dy_pix = ((dY/dH)/2)*3
    width = src.RasterXSize
    height = src.RasterYSize
    path = os.path.dirname(imgfilename)
    # print("path: " + path)
    filename = os.path.basename(imgfilename)
    # print("filename: " + filename)
    name = os.path.splitext(filename)[0]
    # print("name: " + name)
    # print("path: " + path)
    # print(": ",width)
    # print(": ",height)
    mitab = open(path + "/" + name + '.tab', 'wt')
    mitab.write("!table\n")
    mitab.write("!version 300\n")
    mitab.write("!charset WindowsLatin2\n")
    mitab.write("\n")
    mitab.write("Definition Table\n")
    mitab.write("  File \"" + filename + "\"\n")
    mitab.write("  Type \"RASTER\"\n")
    mitab.write("  ("
                + str(int(bbox_l[0]) - dx_pix)
                + ","
                + str(int(bbox_l[3]) + dx_pix)
                + ") (0,0) Label \"Pt 1\",\n")
    mitab.write("  ("
                + str(int(bbox_l[2]) - dy_pix)
                + ","
                + str(int(bbox_l[3]) + dx_pix)
                + ") ("
                + str(width-1)
                + ",0) Label \"Pt 2\",\n")
    mitab.write("  ("
                + str(int(bbox_l[0])-dx_pix)
                + ","
                + str(int(bbox_l[1])+dy_pix)
                + ") (0,"
                + str(height-1)
                + ") Label \"Pt 3\"\n")
    mitab.write("  CoordSys Earth Projection "
                "8, 104, \"m\", 21, 0, 0.9996, 500000, 0\n")
    mitab.write("  Units \"m\"\n")
    mitab.write("begin_metadata\n")
    mitab.write(r"\"\IsReadOnly\" = \"FALSE\"\n")
    mitab.write(r"\"\MapInfo\" = \"\"\n")
    mitab.write(r"\"\MapInfo\TableID\="
                " \"6aebfbb1-0d13-4c6a-8f84-366af9cad985\"\n")
    mitab.write("end_metadata\n")
    mitab.close()


# priprema 2 tipa URL-a za download sa GeoSrbija.rs:
# KATASTAR (kn) i ORTOFOTO (of)
# - hederi, kranje koordinate i veličina slike u pixelima
def gs_url(tip, sloj, bbox):
    global header
    global uuid
    global keys
    global dX
    global dY
    global dW
    global dH
    if tip == "kn":
        dW = 3000
        dH = 3000
        dX = 500
        dY = 500
        # HTTP header za lejere katastra
        header = {'Accept': '*/*',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'en-US,en;q=0.5',
                  'Connection': 'keep-alive',
                  'Cookie': '_ga=GA1.2.853214968.1516814617',
                  'DNT': '1',
                  'Host': 'ogc.geosrbija.rs',
                  'Referer': 'https://a3.geosrbija.rs/',
                  'TE': 'Trailers',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; ' +
                  'Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
                  }
        url = (kn_base_url + "LAYERS=" + sloj
               + "&QUERYABLE=false&TRANSITIONEFFECT=resize&TRANSPARENT=TRUE&"
               "INFOFORMAT=text%2Fhtml&FORMAT=image%2Fpng&VERSION=1.3.0&"
               "EXCEPTIONS=XML&GUI=8&SERVICE=WMS&REQUEST=GetMap&STYLES=&"
               "CRS=EPSG%3A32634&BBOX="
               + bbox
               + "&WIDTH=" + str(dW)
               + "&HEIGHT=" + str(dH)
               )
        return url
    elif tip == "of":
        dW = 2048
        dH = 2048
        dX = 500
        dY = 500
        # HTTP header za lejere ortofoto
        header = {'Accept': 'image/webp,*/*',
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
        uuid = "b71f15d1-d478-4794-ad5e-5bc12f39e415"
        key = "20181025112228"
        url = (of_base_url + "uuid=" + uuid + "&key=" + key + "&LAYERS=" + sloj
               + "&QUERYABLE=false&TRANSITIONEFFECT=resize&TRANSPARENT=TRUE&"
               + "INFOFORMAT=text%2Fplain&FORMAT=image%2Fpng&VERSION=1.1.1&"
               + "SERVICE=WMS&REQUEST=GetMap&STYLES=&SRS=EPSG%3A32634&BBOX="
               + bbox
               + "&WIDTH=" + str(dW)
               + "&HEIGHT=" + str(dH)
               )
        return url


# ažuriranje tabele 'gs_bbox_grid' posle uspešno preuzete PNG slike
# upis vrednosti u odgovarajuću kolonu u zavisnosti od sloja koji se preuzima)
def mreza_gs_update(sloj, vr, bbox):
    cursor.execute(
        sql.SQL(
            "update {} set {} = %s where bbox = %s"
            ).format(
            sql.Identifier(table_name),
            sql.Identifier(sloj)),
        [vr, bbox]
    )
    connection.commit()


# preuzimanje PNG slike sa generisanim URL-om,
# kreiranje odgovarajućih fajlova za georeferencu: WLD, TAB,
# i ažuriranje 'gs_bbox_grid' tabele
def img_download(gs_url, path, imgfilename):
    if not os.path.isfile(path + imgfilename + ".png"):
        # otvaranje WMS linka
        t0 = time.time()
        try:
            print('Slanje zahteva za preuzimanjem...')
            r = requests_retry_session().get(
                gs_url,
                headers=header,
                stream=True
                )
            print('Uspešno!', r.status_code)
        except Exception as x:
            print('Neuspelo preuzimanje :(', x.__class__.__name__)
        else:
            print('Preuzimanje slike...')
            with open(path + imgfilename + ".png", 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(
                        r.iter_content(chunk_size=1024),
                        expected_size=(total_length/1024) + 1):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                f.close()
                print('Preuzimanje gotovo!')
                # kreiranje WLD/PGW fajla
                wld_file(path + imgfilename, bbox_l)
                generate_mitab(path + imgfilename + ".png", bbox_l)
                mreza_gs_update(dl_sloj[c], 1, row[-1])
        finally:
            t1 = time.time()
            print('Trajanje:', t1 - t0, 'sec')
    else:
        print("Kvadrat "+imgfilename+" je već preuzet.")

# =============================================================================
# - Preuzimanje svih 'Bounding Box'-ova iz mreže kvadrata koji imaju status "2"
# -----------------------------------------------------------------------------


# kolone u PostgreSQL tabeli
kolone = {
    'id': 0,            # 1
    'bbox': 0,          # 2
    'mergelist': 0,     # 3
    'min_x': 0,         # 4
    'min_y': 0,         # 5
    'min_x': 0,         # 6
    'min_y': 0          # 7
}

# imena slojeva za preuzimanje i da li se preuzimaju
# 0 - ignioriši sloj,
# 1 - preuzimaj sloj

# KORIGOVATI PROGRAM POSLE DODAVANJA NOVIH KOLONA U gs_bbox_grid TABELI !
# predefinisati "query" (napraviti bolji upit),
# i korigovati  "c < 12" u završnoj petlji - VALJDA NEMA JOŠ NEŠTO :)

gs_slojevi = {
    'of_2010_10cm': ["Orthophoto-10cm_(2007-2010)", "of", 0],      # kompletan
    'of_2013_10cm': ["Orthophoto-10cm_(2011-2013)", "of", 1],      # kompletan
    # 'of_2010_10cm': ["Satelitski_snimci-30cm_2015-2016", "of", 0],# kompletan
    # dodati novu kolonu u PostGIS tabeli i preimenovati ovaj red:
    # 'of_2013_10cm': ["Satelitski_snimci-40cm_2015-2016", "of", 0],
    'of_2010_40cm': ["Orthophoto-40cm_(2007-2010)", "of", 1],
    'of_2013_40cm': ["Orthophoto-40cm_(2011-2013)", "of", 1],
    'parcele': ["layer_532", "kn", 1],    # 532 PARCELE (ISTOK)
    'ulice':    ["layer_32", "kn", 1],    # ULICA
    'objekti': ["layer_280", "kn", 1],    # OBJEKAT
    'kbr':      ["layer_36", "kn", 1],    # KUĆNI BROJ
    'nazivi':   ["layer_54", "kn", 0],    # NAZIVI(DKP)
    'ko':       ["layer_61", "kn", 0],    # KATASTARSKA OPŠTINA
    'naselja':  ["layer_30", "kn", 0],    # NASELJE
    'sst':     ["layer_247", "kn", 0]     # Skupštine stanara
}

kol = list(kolone.keys())

# gs_sloj = list(gs_slojevi.values())
gs_sloj = []
for value in gs_slojevi.values():
    gs_sloj.append(value[0])
# print (gs_sloj)

dl_sloj = list(gs_slojevi.keys())

dl_check = []
for value in gs_slojevi.values():
    dl_check.append(value[2])
# print (dl_check[0])

tipovi = []
for value in gs_slojevi.values():
    tipovi.append(value[1])
# print (tipovi)

query = sql.SQL(
    "select {sl1}, {sl2}, {sl3}, {sl4}, {sl5}, {sl6}, {sl7}, {sl8}, {sl9}, "
    "{sl10}, {sl11}, {sl12}, {kol3}, {kol1}, {kol2}"
    "from {tbl} "
    "where ({sl1} = 2 OR {sl2} = 2 OR {sl3} = 2 OR {sl4} = 2 OR {sl5} = 2 OR "
    "{sl6} = 2 OR {sl7} = 2 OR {sl8} = 2 OR {sl9} = 2 OR {sl10} = 2 OR "
    "{sl11}= 2 OR {sl12} = 2) order by {kol3},{kol1}"
    # and {kol3} > 105"
    ).format(
    tbl=sql.Identifier(table_name),
    sl1=sql.Identifier(dl_sloj[0]),
    sl2=sql.Identifier(dl_sloj[1]),
    sl3=sql.Identifier(dl_sloj[2]),
    sl4=sql.Identifier(dl_sloj[3]),
    sl5=sql.Identifier(dl_sloj[4]),
    sl6=sql.Identifier(dl_sloj[5]),
    sl7=sql.Identifier(dl_sloj[6]),
    sl8=sql.Identifier(dl_sloj[7]),
    sl9=sql.Identifier(dl_sloj[8]),
    sl10=sql.Identifier(dl_sloj[9]),
    sl11=sql.Identifier(dl_sloj[10]),
    sl12=sql.Identifier(dl_sloj[11]),
    kol1=sql.Identifier(kol[0]),
    kol2=sql.Identifier(kol[1]),
    kol3=sql.Identifier(kol[2]))

# print (query.as_string(connection))
cursor.execute(query, ['1'])
# preuzimanje rezultata upita
SQLresult = cursor.fetchall()

# ============================================================================
# - Preuzimanje svih PNG slika sa odgovarajućim BBOX koordinatama
#   i statusom "2" u odgovarajućoj koloni
# ----------------------------------------------------------------------------

for row in SQLresult:
    c = -1
    for i in row:
        c += 1
        if i == 2 and c < 12 and dl_check[c] == 1:
            print(c,
                  " - ",
                  gs_slojevi[dl_sloj[c]][1], " >> ",
                  dl_sloj[c], "-",
                  gs_sloj[c], row[-1], " - ", row[-3],
                  "(", row[-2], ")")
            gsurl = gs_url(gs_slojevi[dl_sloj[c]][1], gs_sloj[c], row[-1])
            print(gsurl)
            bbox_l = row[-1].split(',')
            # print (bbox_l)
            img_filename = dl_sloj[c] + "_" + bbox_l[0] + "_" + bbox_l[1]
            # print(img_filename)
            img_download(gsurl, dl_path + gs_slojevi[dl_sloj[c]][1]
                         + "/" + dl_sloj[c] + "/PNG/", img_filename)
            print("----------------------------------------------------------")

# zatvori konekciju ka bazi
cursor.close()
connection.close()
