from gssetup import kn_base_url
from gssetup import kn_header
from gssetup import A3TKN
from gssetup import of_base_url
from gssetup import of_header
from gssetup import uuid
from gssetup import key
from gssetup import dx
from gssetup import dy
from gssetup import dw
from gssetup import dh
from gssetup import dl_path
from gssetup import gs_slojevi


class GeoSrbijaWMS:
    """Kreiranje WMS URL za GeoSrbija"""

    def __init__(self, sloj, px, py, w=dw, h=dh, xm=dx, ym=dy):
        self.sloj = sloj
        self.px = px
        self.py = py
        self.kx = px + dx
        self.ky = py + dy
        self.w = w
        self.h = h
        self.xm = xm
        self.ym = ym
        self.bbox = (
                     str(px) + "," +
                     str(py) + "," +
                     str(px + dx) + "," +
                     str(py + dy)
                    )

    def __str__(self):
        """User-friendly printing"""
        return f"Sloj: {self.gs_ime} -> bbox: {self.bbox} -> w: {self.w}"

    def __repr__(self):
        """Developer-friendly printing"""
        return f"{self.sloj}, {self.bbox}, {self.w}"

    @property
    def url(self):
        """URL za download PNG mape"""
        if gs_slojevi[self.sloj][1] == 'kn':
            return (kn_base_url +
                    "LAYERS=" + gs_slojevi[self.sloj][0] +
                    "&QUERYABLE=false"
                    "&TRANSITIONEFFECT=resize"
                    "&TRANSPARENT=TRUE&"
                    "INFOFORMAT=text%2Fhtml"
                    "&FORMAT=image%2Fpng"
                    "&VERSION=1.3.0"
                    "&EXCEPTIONS=XML"
                    "&GUI=8"
                    "&A3TKN=" + A3TKN +
                    "&SERVICE=WMS"
                    "&REQUEST=GetMap"
                    "&STYLES=&"
                    "CRS=EPSG%3A32634"
                    "&BBOX=" + self.bbox +
                    "&WIDTH=" + str(self.w) +
                    "&HEIGHT=" + str(self.h)
                    )
        else:
            return (of_base_url +
                    "uuid=" + uuid +
                    "&key=" + key +
                    "&LAYERS=" + gs_slojevi[self.sloj][0] +
                    "&QUERYABLE=false"
                    "&TRANSITIONEFFECT=resize"
                    "&TRANSPARENT=TRUE&"
                    "INFOFORMAT=text%2Fplain"
                    "&FORMAT=image%2Fpng"
                    "&VERSION=1.1.1&"
                    "SERVICE=WMS"
                    "&REQUEST=GetMap"
                    "&STYLES="
                    "&SRS=EPSG%3A32634"
                    "&BBOX=" + self.bbox +
                    "&WIDTH=" + str(self.w) +
                    "&HEIGHT=" + str(self.h)
                    )

    @property
    def header(self):
        """HTTP header za KN i OF"""
        if gs_slojevi[self.sloj][1] == 'kn':
            # HTTP header za lejere katastra
            return kn_header
        else:
            # HTTP header za lejere ortofoto
            return of_header

    @property
    def tip(self):
        return f"{gs_slojevi[self.sloj][1]}"

    @property
    def gs_ime(self):
        return f"{gs_slojevi[self.sloj][0]}"

    @property
    def path(self):
        return (f"{dl_path}"
                f"{gs_slojevi[self.sloj][1]}/"
                f"{self.sloj}/"
                f"PNG/")

    @property
    def filename(self):
        # return f"{self.sloj}_{self.px}_{self.py}_{self.w}px_{dx}m"
        return f"{self.sloj}_{self.px}_{self.py}"
