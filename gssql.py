"""
# ============================================================================
# Generisanje mreže kvadrata u PostGIS bazi za organizovanje preuzimanja
# Ortofoto podloga sa portala GeoSrbija https://a3.geosrbija.rs


# Radi lakšeg upravljanja preuzetih podloga definisana je oblast u kojoj je
# moguće vršiti preuzimanje. Teritorija/oblast je podeljena na mrežu kvadrata
# gde max dužina i visina jednog kvadrata (dX i dY) zavisi od toga koji se sloj
# preuzima tj. zbog postavljenih ograničenja na WMS serveru portala:

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

# ============================================================================
# - Definisanje oblasti za preuzimanje: polazne i krajnje koordinate
# po X i Y osi (EPSG: 32634)

# maksimalne koordinate za Naissus:
# stax = 558000
# endx = 616500
# stay = 4763000
# endy = 4814500
# ============================================================================
"""

# import sys
import psycopg2
from psycopg2 import sql
from datetime import datetime

server = 'localhost'
# server = 'VERDI'
baza = 'geosrbija'
user = 'postgres'
password = 'softdesk'
table_name = 'gs_bbox_grid'

try:
    # PostgreSQL konekcija - kućni server vs jkp "Naissus
    connection = psycopg2.connect(
        dbname=baza,
        user=user,
        host=server,
        password=password
        )
    cursor = connection.cursor()
except psycopg2.OperationalError as e:
    print(95*"=")
    print(95*"-")
    print(f"{e}")
    print(95*"-")
    db_status = (f" - Konekcija sa bazom nije moguća!\n"
                 f"   Da li je server '{server}' dostupan?\n"
                 f"   Funkcije za rad sa bazom podataka neće biti dostupne.")
    # sys.exit(1)
else:
    db_status = f"Konekcija sa serverom '{server}' uspostavljena!"


def sql_tabela():
    """Kreiranje tabele [gs_bbox_grid]"""
    pass


def sql_insert_kvadrat(id_kvad, bbox_kvad, datum, dl, min_x, min_y, max_x,
                       max_y, crs, mergelist, geom):
    """
    Insertovanje kvadrata u PostGIS bazi i popunjavanje atributima za isti.
    """
    sql_command = (
                    "INSERT INTO public.gs_bbox_grid "
                    "(id, bbox, mergelist, datum, min_x, min_y, max_x, max_y,"
                    " sp_geometry) "
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


def sql_generator_mreze(stax, stay, endx, endy, d):
    """
    Generisanje parova koordinata za kvadrate i poziv SQL komande za insert.
    """
    c = 10000
    # kalkulakcija bbox
    for n in range(stax, endx, d):
        for i in range(stay, endy, d):
            bboxl = []
            c = c + 1
            bboxl.append(n)
            bboxl.append(i)
            bboxl.append(n+d)
            bboxl.append(i+d)
            bbox = ",".join(str(e) for e in bboxl)
            wkt = (
                "\'POLYGON(("
                + str(bboxl[0]) + " "
                + str(bboxl[1]) + ", "
                + str(bboxl[0]) + " "
                + str(bboxl[3]) + ", "
                + str(bboxl[2]) + " "
                + str(bboxl[3]) + ", "
                + str(bboxl[2]) + " "
                + str(bboxl[1]) + ", "
                + str(bboxl[0]) + " "
                + str(bboxl[1]) +
                "))\'"
                )
            sql_insert_kvadrat(c, str(bbox), str(datetime.now()), 0,
                               str(bboxl[0]), str(bboxl[1]),
                               str(bboxl[2]), str(bboxl[3]),
                               'EPSG:32634', 0,
                               "ST_PolygonFromText("+wkt+",32634)"
                               )

    print("Generisano je " + str(c-10000) + " kvadrata!")
    # zatvori konekciju ka bazi
    cursor.close()
    connection.close()


def sql_update_mreza(sloj, vr, bbox):
    """
    Ažuriranje tabele 'gs_bbox_grid' posle uspešno preuzete PNG slike i
    upis vrednosti u odgovarajuću kolonu u zavisnosti od sloja koji se
    preuzima.
    """
    cursor.execute(
        sql.SQL(
                "UPDATE {} SET {} = %s WHERE BBOX = %s"
               ).format(
                        sql.Identifier(table_name),
                        sql.Identifier(sloj)
                        ), [vr, bbox]
                  )
    connection.commit()


def sql_kvadrat_id(table, id):
    query_id = sql.SQL(
                       "SELECT {}, {}, {}, {}, {} FROM {} WHERE {} = %s"
                       ).format(
                                sql.Identifier('min_x'),
                                sql.Identifier('min_y'),
                                sql.Identifier('max_x'),
                                sql.Identifier('max_y'),
                                sql.Identifier('mergelist'),
                                sql.Identifier(table),
                                sql.Identifier('mi_prinx')
                                )

    cursor.execute(query_id, [id])
    sql_result = cursor.fetchall()

    for row in sql_result:
        return row


def sql_merge_id(table, id):
    query_id = sql.SQL(
                       "SELECT {} FROM {} WHERE {} = %s ORDER BY {}"
                       ).format(
                                sql.Identifier('id'),
                                sql.Identifier(table),
                                sql.Identifier('mergelist'),
                                sql.Identifier('id')
                                )
    cursor.execute(query_id, [id])
    sql_result = cursor.fetchall()

    kvads = [row[0] for row in sql_result]
    return kvads
