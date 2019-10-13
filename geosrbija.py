"""
===============================================================================
Preuzimanje podloga sa GeoSrbija portala
https://a3.geosrbija.rs
-------------------------------------------------------------------------------

    verzija:  2.0
    datum:    2019-OKTOBAR-12
    autor: Nebojša Pešić, dipl. građ. ing (nmiTools@gmail.com)

 preduslovi:
    Python 3.x (scoop reset python)
    pip install psycopg2
    pip install requests
    pip install clint
    pip install M:/MEGAsync/Python/whl/GDAL-3.0.1-cp37-cp37m-win_amd64.whl

===============================================================================
"""

import sys
import os
import argparse

from gsmreza import genmreza
from gssetup import ver

os.system('cls')


def mreža(arguments):
    print(f"Kreiranje mreže koordinatnih kvadrata sa parametrima:")
    print(f" - px = {arguments.px}")
    print(f" - py = {arguments.py}")
    print(f" - kx = {arguments.kx}")
    print(f" - ky = {arguments.ky}")
    print(f" - d  = {arguments.d}m")
    genmreza(arguments.px, arguments.py, arguments.kx, arguments.ky, arguments.d)


def kvadrat(arguments):
    print(f"Preuzimanje kvadrata broj {arguments.id} ...")


if __name__ == "__main__":

    # Pokretanje programa i ispis imena i verzije
    print(80*"=")
    print(f"GeoSrbija Downloader v{ver}")
    print(80*"-")
    
    if len(sys.argv) >= 2:
        # top-level parser
        parser = argparse.ArgumentParser(prog='GeoSrbija',
                                         description="Preuzimanje podloga sa GeoSrbija portala.")
        
        subparsers = parser.add_subparsers()

        # ---------------------------------------------------------------------------------------------------
        # parser za komandu 'mreža'

        par_kvadrat = subparsers.add_parser('mreža',
                                            description='Kreiranje mreže koordinatnih kvadrata (EPSG:32634).')
        par_kvadrat.add_argument('px',
                                 type=int,
                                 help='Početna X koordinata')
        par_kvadrat.add_argument('py',
                                 type=int,
                                 help='Početna Y koordinata')
        par_kvadrat.add_argument('kx',
                                 type=int,
                                 help='Krajnja X koordinata')
        par_kvadrat.add_argument('ky',
                                 type=int,
                                 help='Krajnja Y koordinata')
        par_kvadrat.add_argument('-d',
                                 type=int,
                                 default=500,
                                 help='Dužina stranice kvadrata u metrima')
        par_kvadrat.set_defaults(func=mreža)

        # ---------------------------------------------------------------------------------------------------
        # parser za komandu 'kvadrat'

        par_kvadrat = subparsers.add_parser('kvadrat',
                                            description='Preuzimanje numerisanog kvadrata iz mreže podloga.')
        par_kvadrat.add_argument('id',
                                 type=int,
                                 help=' ID broj kvadrata u mreži')
        par_kvadrat.set_defaults(func=kvadrat)

        # ---------------------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------------------

        arguments = parser.parse_args()
        arguments.func(arguments)

    else:

        print("Niste naveli nijedan komandni parametar.\n"
              "Za pomoć otkucajte 'python geosrbija.py -h'")




"""
# staX = 568500
# endX = 573500
# staY = 4785000
# endY = 4787500

python geosrbija.py mreža 568500, 4785000, 573500, 4787500

================================================================================
GeoSrbija Downloader v2.0
--------------------------------------------------------------------------------
Kreiranje mreže koordinatnih kvadrata sa parametrima:
 - px = 568500
 - py = 4785000
 - kx = 573500
 - ky = 4787500
 - d  = 500m
Generisano je 50 kvadrata!
 """
    


    