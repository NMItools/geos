"""
# =============================================================================
# Generisanje mreže kvadrata u PostGIS bazi za organizovanje preuzimanja
# Ortofoto podloga sa portala GeoSrbija

# https://a3.geosrbija.rs

# -----------------------------------------------------------------------------

    verzija:  2.0
    datum:    2019-MART-14
    autor: Nebojša Pešić, dipl. građ. ing (nmiTools@gmail.com)

# ============================================================================
# Radi lakšeg upravljanja preuzetih podloga definisana je oblast u kojoj je
# moguće vršiti preuzimanje. Teritorija/oblast je podeljena na mrežu kvadrata
# gde max dužina i visina jednog kvadrata (dX i dY) zavisi od toga koji se sloj
# preuzima tj. zbog postavljenih ograničenja na WMS serveru portala:
# ----------------------------------------------------------------------------
# - Ortofoto

# Max dozvoljena širina/visina slike: 4096 pixela (ograničenje WMS servera)
# Stavljamo duplo manju vrednost jer server ima problema da izgeneriše
# maksimalu sliku (~45 MB) i često ne uspeva da obradi zahtev.
# dWof = 2048
# dHof = 2048

# Max dimenzija po X/Y osi: 500 metara (najveće dozvoljeno uvećanje/ZOOM;
# 1 pixel = 0.1220703125 metara)
# dXof = 500
# dYof = 500

# =============================================================================
# - Definisanje oblasti za preuzimanje: polazne i krajnje koordinate
# po X i Y osi (EPSG: 32634)

# maksimalne koordinate za Naissus:
# staX = 558000
# endX = 616500
# staY = 4763000
# endY = 4814500
# =============================================================================
"""

from datetime import datetime
from gssetup import connection
from gssetup import cursor


def sql_kvadrat(
    id_kvad,
    bbox_kvad,
    datum, dl,
    min_x,
    min_y,
    max_x,
    max_y,
    crs,
    mergelist,
    geom
        ):
        """ Insertovanje kvadrata u PostGIS bazi i popunjavanje atributima za isti """
        sql_command = (
                       "INSERT INTO public.gs_bbox_grid "
                       "(id, bbox, mergelist, datum, min_x, min_y, max_x, max_y, sp_geometry) "
                       "VALUES ("
                       + str(id_kvad) + ", \'"
                       + bbox_kvad + "\', \'" 
                       + str(0) + "\', \'" 
                       + datum + "\', " 
                       + min_x + ", " 
                       + min_y + ", "
                       + max_x + ", "
                       + max_y + ", "
                       + geom + ")"
                       )
        # print(sql_command)
        cursor.execute(sql_command)
        connection.commit()


def genmreza(staX, staY, endX, endY, d):
    """ Generisanje parova koordinata za kvadrate i poziv SQL komande za insert """
    c = 10000
    # kalkulakcija bbox
    for n in range(staX, endX, d):
        for i in range(staY, endY, d):
            bboxL=[]
            c = c + 1
            bboxL.append(n)
            bboxL.append(i)
            bboxL.append(n+d)
            bboxL.append(i+d)
            bbox = ",".join(str(e) for e in bboxL)
            wkt = (
                "\'POLYGON(("
                + str(bboxL[0]) + " "
                + str(bboxL[1]) + ", "
                + str(bboxL[0]) + " "
                + str(bboxL[3]) + ", "
                + str(bboxL[2]) + " "
                + str(bboxL[3]) + ", "
                + str(bboxL[2]) + " "
                + str(bboxL[1]) + ", "
                + str(bboxL[0]) + " "
                + str(bboxL[1]) +
                "))\'"
                )
            sql_kvadrat(c, str(bbox), str(datetime.now()), 0, str(bboxL[0]), str(bboxL[1]), str(bboxL[2]), str(bboxL[3]), 'EPSG:32634', 0, "ST_PolygonFromText("+wkt+",32634)")

    print ("Generisano je "+ str(c-10000) + " kvadrata!")
    # zatvori konekciju ka bazi
    cursor.close()
    connection.close()
