"""
# =====================================================================================================
# Kreiranje listi za spajanje više preuzetih *.PNG kvadrata u jedan veći
# https://a3.geosrbija.rs
# -----------------------------------------------------------------------------------------------------

    verzija:  2.0
    datum:    2018-MAJ-05
    autor: Nebojša Pešić, dipl. građ. ing (nmiTools@gmail.com)

Krajnji rezultat rada ove skripte je kreiranje liste preuzetih PNG kvadrata nekog sloja sa WMS servera
GeoSrbije koji se trebaju spojiti u veći kvadrat.

Lista se snima u TXT fajl koji će biti pomoćni fajl za GDAL/OGR komandu koja će vršiti spajanje.

Spajanje više PNG kvadrata u jedan veći se radi zbog optimizacije rada sa podlogama, budući da ih ima
više hiljada a trebaju se publikovati preko GeoServera.
# =====================================================================================================
"""
import psycopg2
from psycopg2 import sql
from psycopg2 import extensions as ext
import os

# brisanje ekrana
os.system('cls')

# ---------------------------------------------------------------------------------------------------
#   PostGIS konekcija - kućni server vs jkp "Naissus"

# server = 'localhost'
server = 'VERDI'
baza = 'geosrbija'
user = 'postgres'
password = 'softdesk'
table_name = 'gs_bbox_grid'

connection = psycopg2.connect(dbname=baza, user=user, host=server, password=password)
# print(connection)
cur = connection.cursor()

# ---------------------------------------------------------------------------------------------------
# Kreiranje praznih listi za upisivanje potrebnih parametara

preuzmi=[]
mlist=[]

# imena kolona u postgis tabeli koja su nam potrebna za generisanje imena PNG fajlova

columns = ['mergelist', 'min_x', 'min_y' ]

# Setovanje direktorijuma

of_dir = r"D:/geosrbija/of/"
# kn_dir = r"D:/geosrbija/kn/"
kn_dir = of_dir


# slojevi koji će se koristiti za kreiranje "mergelist"-a
# 0 - ne kreiraj
# 1 - kreiraj

of_slojevi = {
    'of_2010_10cm': 0,
    'of_2013_10cm': 0,
    'of_2010_40cm': 1,
    'of_2013_40cm': 1}

kn_slojevi = {
    'parcele': 0,
    'ulice': 0,
    'objekti': 0,
    'kbr': 0,
    'nazivi': 0,
    'ko': 0,
    'naselja': 0,
    'sst': 0}

# ---------------------------------------------------------------------------------------------------
# preuzimanje id brojeva svih definisanih "mergelist" kvadrata za spajanje podloga
# ("mergelist" kolona u PostGIS tabeli gs_bbox_grid)

# definicija upita
query_1 = sql.SQL(
    "select distinct {col} from {tbl} where {mlist} > %s order by {mlist}"
    ).format(
        col = sql.Identifier (columns[0]),
        tbl = sql.Identifier(table_name),
        mlist = sql.Identifier(columns[0]))

print(query_1.as_string(connection))
# # select distinct "mergelist" from "gs_bbox_grid" where "mergelist" > %s order by "mergelist"

# izvršavanje upita u bazi
cur.execute(query_1, ['0'])

# preuzimanje rezultata upita
SQLresult_1 = cur.fetchall()

# kreiranje liste od ID brojeva "mergelist" kvadrata
for row in SQLresult_1:
    mlist.append(row[0])
print (mlist)

# ---------------------------------------------------------------------------------------------------
# preuzimanje BBOX-ova svih manjih kvadrata koji čine novi ukrupnjeni kvadrat

query_2 = sql.SQL(
    "select {col} from {tbl} where {mlist} = %s order by {mlist}"
    ).format(
        col = sql.SQL(', ').join(map(sql.Identifier, columns)),
        tbl = sql.Identifier(table_name),
        mlist = sql.Identifier(columns[0]))

print(query_2.as_string(connection))
# # select "mergelist", "min_x", "min_y" from "gs_bbox_grid" where "mergelist" = %s order by "mergelist"

# ---------------------------------------------------------------------------------------------------
# za spisak odabranih slojeva...
s = 0

for sloj in {v for v in of_slojevi.items() if v[1] == 1}:
    print("==================================================================")
    print (sloj[0])
    s = s + 1
    # kreiraj tekstualni fajl u odgovarajući folder za taj sloj
    # koji se odnosi na određenu grupu za spajanje ("mergelist")...
    for m in mlist:
        print("Kreiranje mergelist_" + str(m) + "...")
        f = open(kn_dir + sloj[0] + "/PNG/" + "mergelist_" + str(m) + '.txt', 'wt')
        cur.execute(query_2, [m])
        SQLresult_2 = cur.fetchall()
        # i u njega upiši spisak svih podloga
        for row in SQLresult_2:
            f.write(sloj[0] + "_"+str(row[1])+"_"+str(row[2])+".png\n")
        f.close()

# u = s * m
# print("Kreirano je "+str(s)+" x "+str(m)+" = "+str(u) + " lista spajanja!")

connection.commit()
connection.close()
