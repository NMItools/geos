import osgeo.gdal as gdal
from gssetup import dx, dy


def gen_wld_file(wmst):
    """
    kreiranje WLD/PGW fajla za georeferencu rastera
    """
    with open(wmst.path + wmst.filename + '.pgw', 'w') as wld:
        wld.write(str(dx/wmst.w)+"\n")
        wld.write("0.00000000\n")
        wld.write("0.00000000\n")
        wld.write(str(-(dy/wmst.h))+"\n")
        wld.write(str(wmst.px)+"\n")
        wld.write(str(wmst.ky)+"\n")

    print(f"Kreiran WLD fajl za georeferencu rastera.")


def gen_tab_file(wmst):
    """
    kreiranje MapInfo TAB fajla za georeferencu rastera
    """
    try:
        src = gdal.Open(wmst.path + wmst.filename + ".png")
        width = src.RasterXSize
        height = src.RasterYSize
    except AttributeError:
        print("Problem sa preuzetim fajlom!")
        return False
    dx_pix = (dx/wmst.w)/2
    dy_pix = ((dy/wmst.h)/2)*3
    filename = wmst.filename + ".png"
    with open(wmst.path + wmst.filename + '.tab', 'wt') as mitab:
        mitab.write("!table\n")
        mitab.write("!version 300\n")
        mitab.write("!charset WindowsLatin2\n")
        mitab.write("\n")
        mitab.write("Definition Table\n")
        mitab.write("  File \"" + filename + "\"\n")
        mitab.write("  Type \"RASTER\"\n")
        mitab.write("  ("
                    + str(wmst.px - dx_pix)
                    + ","
                    + str(wmst.ky + dx_pix)
                    + ") (0,0) Label \"Pt 1\",\n")
        mitab.write("  ("
                    + str(wmst.kx - dy_pix)
                    + ","
                    + str(wmst.ky + dx_pix)
                    + ") ("
                    + str(width - 1)
                    + ",0) Label \"Pt 2\",\n")
        mitab.write("  ("
                    + str(wmst.px - dx_pix)
                    + ","
                    + str(wmst.py + dy_pix)
                    + ") (0,"
                    + str(height - 1)
                    + ") Label \"Pt 3\"\n")
        mitab.write("  CoordSys Earth Projection "
                    "8, 104, \"m\", 21, 0, 0.9996, 500000, 0\n")
        mitab.write("  Units \"m\"\n")
        mitab.write("begin_metadata\n")
        mitab.write("\"" + "\\" + 'IsReadOnly' + "\"" + " = " + "\"" + 'FALSE'
                    + "\"\n")
        mitab.write("\"" + "\\" + 'MapInfo' + "\"" + " = " + "\"" + "\"\n")
        mitab.write("\"" + "\\" + 'MapInfo' + "\\" + 'TableID' + "\"" + " = "
                    + "\"" + '6aebfbb1-0d13-4c6a-8f84-366af9cad985' + "\"\n")
        mitab.write("end_metadata\n")

    print(f"Kreiran MapInfo TAB fajla za georeferencu rastera.")
