import os

os.system('cls')

id_kvad = '9999'
bbox_kvad = 'x1, y1, x2, y2'
datum = '1973-10-16 00:00:00+02'
dl = '1'
min_x = '568500'
min_y = '4785000'
max_x = '573500'
max_y = '4787500'
crs = '32634'
mergelist = '999'
geom = 'GEOMETRY'


sql_command = ("INSERT INTO public.gs_bbox_grid "
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
               + geom + ")")
print(sql_command)

bboxL = [1, 2, 3, 4]

# "\'POLYGON(("

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
print(wkt)