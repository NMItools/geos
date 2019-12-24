REM ======================================================================
REM # staX = 568500
REM # endX = 573500
REM # staY = 4785000
REM # endY = 4787500

REM ================================================================================
REM GeoSrbija Downloader v2.0
REM --------------------------------------------------------------------------------
REM Kreiranje mreže koordinatnih kvadrata sa parametrima:
 REM - px = 568500
 REM - py = 4785000
 REM - kx = 573500
 REM - ky = 4787500
 REM - d  = 500m
REM Generisano je 50 kvadrata!

REM -------------------------------------------------------------------------------------------

REM from gssetup import table_name
REM from gssetup import connection
REM from gssetup import cursor

REM from gssql import sql_merge_id
REM from gssql import sql_kvadrat_id

REM table_name
REM 'gs_bbox_grid'

REM sql_kvadrat_id(table_name, 532)
REM (22, 0, 558000, 4793000)

REM sql_merge_id(table_name, 10)

REM -------------------------------------------------------------------------------------------

python geos.py mreža 568500, 4785000, 573500, 4787500

python geos.py bbox of_2013_40cm, 569000, 4790500
python geos.py bbox test 569000, 4790500

python geos.py id gs_bbox_grid 23 parcele

python geos.py ml gs_bbox_grid 10 parcele
python geos.py ml gs_bbox_grid 10 objekti
python geos.py ml gs_bbox_grid 81 parcele_jug
python geos.py ml gs_bbox_grid 82 parcele_jug

REM trg vojske i dr petra vucinica
python geos.py bbox of_2013_10cm, 572000, 4796500
python geos.py bbox of_2013_40cm, 572000, 4796500

python geos.py id gs_bbox_grid 1349 parcele

python geos.py ml gs_bbox_grid 48 parcele