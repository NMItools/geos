"""
==============================================================================
Preuzimanje podloga sa GeoSrbija portala https://a3.geosrbija.rs
------------------------------------------------------------------------------

    verzija:  2.0
    datum:    2019-OKTOBAR-12
    autor: Nebojša Pešić, dipl. građ. ing (nmiTools@gmail.com)

 preduslovi:
    Python 3.x (scoop reset python)
    pip install psycopg2
    pip install requests
    pip install clint
    pip install M:/MEGAsync/Python/whl/GDAL-3.0.1-cp37-cp37m-win_amd64.whl

==============================================================================
"""

import sys
import os
import argparse

from gssetup import verzija
from gssetup import slojevi
from gssql import db_status
from gssql import sql_generator_mreze
from gssql import sql_kvadrat_id
from gssql import sql_merge_id
from gsdownload import img_download
from gsfiles import gen_wld_file
from gsfiles import gen_tab_file

from gswms import GeoSrbijaWMS

os.system('cls')


def mreža(args):
    print(f"Kreiranje mreže koordinatnih kvadrata sa parametrima:")
    print(f" - px = {args.px}")
    print(f" - py = {args.py}")
    print(f" - kx = {args.kx}")
    print(f" - ky = {args.ky}")
    print(f" - d  = {args.d}m")
    sql_generator_mreze(args.px, args.py,
                        args.kx, args.ky,
                        args.d)


def bbox(args):
    wmst = GeoSrbijaWMS(args.sloj, args.x, args.y)
    print(f"Preuzimanje bbox kvadrata [{wmst}]")
    if img_download(wmst):
        gen_wld_file(wmst)
        gen_tab_file(wmst)


def id(args):
    qid = sql_kvadrat_id(args.tabela, args.ID)
    wmst = GeoSrbijaWMS(args.sloj, qid[0], qid[1])
    print(f"Preuzimanje kvadrata ID = {args.ID} - [{wmst}]")
    if img_download(wmst):
        gen_wld_file(wmst)
        gen_tab_file(wmst)


def ml(args):
    qmid = sql_merge_id(args.tabela, args.MID)
    c = 1
    for id in qmid:
        qid = sql_kvadrat_id(args.tabela, id)
        wmst = GeoSrbijaWMS(args.sloj, qid[0], qid[1])
        print(f"Preuzimanje ML = {args.MID} | {id} ({c}/{len(qmid)})")
        if img_download(wmst):
            gen_wld_file(wmst)
            gen_tab_file(wmst)
            c += 1


if __name__ == "__main__":

    # Pokretanje programa i ispis imena i verzije
    print(95*"=")
    print(f"GeoSrbija Downloader v{verzija}")
    print(95*"-")
    print(db_status)
    print(95*"-")

    if len(sys.argv) >= 2:
        # top-level parser
        parser = argparse.ArgumentParser(prog='GeoSrbija',
                                         description="Preuzimanje podloga sa "
                                                     "GeoSrbija portala. "
                                                     "\na3.geosrbija.org")

        subparsers = parser.add_subparsers()

        # --------------------------------------------------------------------
        # parser za komandu 'mreža'

        par_mreza = subparsers.add_parser('mreža',
                                          description="Kreiranje mreže "
                                          "koordinatnih kvadrata"
                                          "(EPSG:32634)."
                                          )
        par_mreza.add_argument('px',
                               type=int,
                               help='Početna X koordinata')
        par_mreza.add_argument('py',
                               type=int,
                               help='Početna Y koordinata')
        par_mreza.add_argument('kx',
                               type=int,
                               help='Krajnja X koordinata')
        par_mreza.add_argument('ky',
                               type=int,
                               help='Krajnja Y koordinata')
        par_mreza.add_argument('-d',
                               type=int,
                               default=500,
                               help='Dužina stranice kvadrata u metrima')
        par_mreza.set_defaults(func=mreža)

        # --------------------------------------------------------------------
        # parser za komandu 'bbox'

        par_bbox = subparsers.add_parser('bbox',
                                         description="Preuzimanje "
                                                     " kvadrata na osnovu"
                                                     " koordinate donjeg"
                                                     " levog ugla.")
        par_bbox.add_argument('sloj',
                              choices=slojevi,
                              help='tip sloja na GeoSrbija')
        par_bbox.add_argument('x',
                              type=int,
                              help='donja leva X koordinata kvadrata')
        par_bbox.add_argument('y',
                              type=int,
                              help='donja leva Y koordinata kvadrata')
        par_bbox.set_defaults(func=bbox)

        # --------------------------------------------------------------------
        # parser za komandu 'id'
        par_id = subparsers.add_parser('id',
                                       description="Preuzimanje "
                                                   " kvadrata na osnovu"
                                                   " njegovog ID u "
                                                   " mreži.")
        par_id.add_argument('tabela',
                            type=str,
                            help='ime tabele u bazi za mrežu')
        par_id.add_argument('ID',
                            type=int,
                            help='ID kvadrata u mreži')
        par_id.add_argument('sloj',
                            choices=slojevi,
                            help='tip sloja na GeoSrbija')
        par_id.set_defaults(func=id)

        # --------------------------------------------------------------------
        # parser za komandu 'ml'
        par_ml = subparsers.add_parser('ml',
                                       description="Preuzimanje "
                                                   " metakvadrata na osnovu"
                                                   " njegovog broja u "
                                                   " mreži.")
        par_ml.add_argument('tabela',
                            type=str,
                            help='ime tabele u bazi za mrežu')
        par_ml.add_argument('MID',
                            type=int,
                            help='ID metakvadrata u mreži')
        par_ml.add_argument('sloj',
                            choices=slojevi,
                            help='tip sloja na GeoSrbija')
        par_ml.set_defaults(func=ml)

        args = parser.parse_args()
        args.func(args)

    else:

        print("Niste naveli nijedan komandni parametar.\n"
              "Za pomoć otkucajte 'python geosrbija.py -h'")
