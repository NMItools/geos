import os

os.system('cls')

# id_kvad = '9999'
# bbox_kvad = 'x1, y1, x2, y2'
# datum = '1973-10-16 00:00:00+02'
# dl = '1'
# min_x = '568500'
# min_y = '4785000'
# max_x = '573500'
# max_y = '4787500'
# crs = '32634'
# mergelist = '999'
# geom = 'GEOMETRY'


# sql_command = ("INSERT INTO public.gs_bbox_grid "
#                "(id, bbox, mergelist, datum, min_x, min_y, max_x, max_y, sp_geometry) "
#                "VALUES ("
#                + str(id_kvad) + ", \'"
#                + bbox_kvad + "\', \'" 
#                + str(0) + "\', \'" 
#                + datum + "\', " 
#                + min_x + ", " 
#                + min_y + ", "
#                + max_x + ", "
#                + max_y + ", "
#                + geom + ")")
# print(sql_command)

# bboxL = [1, 2, 3, 4]

# # "\'POLYGON(("

# wkt = (
#        "\'POLYGON(("
#        + str(bboxL[0]) + " "
#        + str(bboxL[1]) + ", "
#        + str(bboxL[0]) + " "
#        + str(bboxL[3]) + ", "
#        + str(bboxL[2]) + " "
#        + str(bboxL[3]) + ", "
#        + str(bboxL[2]) + " "
#        + str(bboxL[1]) + ", "
#        + str(bboxL[0]) + " "
#        + str(bboxL[1]) +
#        "))\'"
#        )
# print(wkt)

# gs_slojevi = {
#     # 'of_2010_10cm': ["Orthophoto-10cm_(2007-2010)", "of", 0],
#     # 'of_2013_10cm': ["Orthophoto-10cm_(2011-2013)", "of", 1],
#     # 'of_2010_10cm': ["Satelitski_snimci-30cm_2015-2016", "of", 0],
#     #  dodati novu kolonu u PostGIS tabeli i preimenovati ovaj red:
#     # 'of_2013_10cm': ["Satelitski_snimci-40cm_2015-2016", "of", 0],
#     # 'of_2010_40cm': ["Orthophoto-40cm_(2007-2010)", "of", 1],
#     # 'of_2013_40cm': ["Orthophoto-40cm_(2011-2013)", "of", 1],
#     'parcele': ["layer_532", "kn", 1],    # 532 PARCELE (ISTOK)
#     'ulice':    ["layer_32", "kn", 1],    # ULICA
#     'objekti': ["layer_280", "kn", 1],    # OBJEKAT
#     'kbr':      ["layer_36", "kn", 1],    # KUĆNI BROJ
#     'nazivi':   ["layer_54", "kn", 0],    # NAZIVI(DKP)
#     'ko':       ["layer_61", "kn", 0],    # KATASTARSKA OPŠTINA
#     'naselja':  ["layer_30", "kn", 0],    # NASELJE
#     'sst':     ["layer_247", "kn", 0]     # Skupštine stanara
# }

# print(gs_slojevi['parcele'][1])

# for value in gs_slojevi.values():
#        print(value[0])

# from gswms import GeoSrbijaWMS
# wms = GeoSrbijaWMS('parcele', 569000, 4790500)

# wms
# parcele, 569000,4790500,569500,4791000, 3000

# Sloj: parcele -> bbox: 569000,4790500,569500,4791000 -> w: 3000

# wms.url
# 'https://ogc.geosrbija.rs/mapserv.ashx?LAYERS=layer_532&QUERYABLE=false&TRANSITIONEFFECT=resize&TRANSPARENT=TRUE&INFOFORMAT=text%2Fhtml&FORMAT=image%2Fpng&VERSION=1.3.0&EXCEPTIONS=XML&GUI=8&A3TKN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoibWFwc2VydmVyIiwibmJmIjoxNTcxMDQ0NTA1LCJleHAiOjE1NzEzOTAxMDUsImlhdCI6MTU3MTA0NDUwNX0.kmzjR5sLGe47rSUJgqPuZ5_ZK2wwx1eEfgePIkntwGE&SERVICE=WMS&REQUEST=GetMap&STYLES=&CRS=EPSG%3A32634&BBOX=569000,4790500,569500,4791000&WIDTH=3000&HEIGHT=3000'

# wms.header
# {'Accept': 'image/webp,*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive', 'Cookie': '_ga=GA1.2.122374505.1511963246; _gid=GA1.2.722972071.1571044509', 'DNT': '1', 'Host': 'ogc.geosrbija.rs', 'Referer': 'https://a3.geosrbija.rs/', 'TE': 'Trailers', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}

# wms.tip
# 'kn'

# wms.gs_ime
# 'layer_532'

# wms.path  
# 'D:/geosrbija/kn/parcele/PNG/'

# wms.filename
# 'parcele_569000_4790500'

# ------------------------------------------------------------------
# wms = GeoSrbijaWMS('objekti', 569000, 4790500)  

# wms.filename
# 'objekti_569000_4790500'

# wms.path     
# 'D:/geosrbija/kn/objekti/PNG/'

# wms.gs_ime
# 'layer_280'

# wms.tip    
# 'kn'

# wms.header
# {'Accept': 'image/webp,*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive', 'Cookie': '_ga=GA1.2.122374505.1511963246; _gid=GA1.2.722972071.1571044509', 'DNT': '1', 'Host': 'ogc.geosrbija.rs', 'Referer': 'https://a3.geosrbija.rs/', 'TE': 'Trailers', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}

# wms.url    
# 'https://ogc.geosrbija.rs/mapserv.ashx?LAYERS=layer_280&QUERYABLE=false&TRANSITIONEFFECT=resize&TRANSPARENT=TRUE&INFOFORMAT=text%2Fhtml&FORMAT=image%2Fpng&VERSION=1.3.0&EXCEPTIONS=XML&GUI=8&A3TKN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoibWFwc2VydmVyIiwibmJmIjoxNTcxMDQ0NTA1LCJleHAiOjE1NzEzOTAxMDUsImlhdCI6MTU3MTA0NDUwNX0.kmzjR5sLGe47rSUJgqPuZ5_ZK2wwx1eEfgePIkntwGE&SERVICE=WMS&REQUEST=GetMap&STYLES=&CRS=EPSG%3A32634&BBOX=569000,4790500,569500,4791000&WIDTH=3000&HEIGHT=3000'

# print(wms)
# Sloj: objekti -> bbox: 569000,4790500,569500,4791000 -> w: 3000

# wms        
# objekti, 569000,4790500,569500,4791000, 3000

# def img_download(url, header, path, filename):
#     """
#     preuzimanje PNG slike sa generisanim URL-om,
#     kreiranje odgovarajućih fajlova za georeferencu: WLD, TAB,
#     i ažuriranje 'gs_bbox_grid' tabele

#     """
#     if not os.path.isfile(path + filename + ".png"):
#         t0 = time.time()
#         # otvaranje WMS linka
#         try:
#             print('Slanje zahteva za preuzimanjem...')
#             r = requests_retry_session().get(url, headers=header, stream=True)
#             print('Uspešno!', r.status_code)
#         except Exception as x:
#             print('Neuspeli zahtev :(', x.__class__.__name__)
#         else:
#             print('Preuzimanje slike...')
#             with open(path + filename + ".png", 'wb') as f:
#                 total_length = int(r.headers.get('content-length'))
#                 for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
#                     if chunk:
#                         f.write(chunk)
#                         f.flush()
#                 f.close()
#                 print('Preuzimanje gotovo!')
#                 # kreiranje WLD/PGW fajla
#                 gen_wld_file(path + filename, bbox_l)
#                 gen_tab_file(path + filename + ".png", bbox_l)
#                 mreza_gs_update(dl_sloj[c], 1, row[-1])
#         finally:
#             t1 = time.time()
#             print('Trajanje:', t1 - t0, 'sec')
#     else:
#         print("Kvadrat "+filename+" je već preuzet.")

print("\"")