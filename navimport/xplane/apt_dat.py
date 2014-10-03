#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#
# Better remove the bad design with the globals instead. Thanks.

import os
import sys
from geographiclib.geodesic import Geodesic

from navimport import conf
from navimport import db
from navimport import utils as ut

ESTIMATED_LINES = 2470000  # almost 2.5 million

QUIRK = "QUIRK"
"""A quirky variable - returned to avoid erro for now"""

FT_2_M = 0.3048
"""Mutliplier for feet to metres"""


class Apt:
    """Import helper for an airport"""

    def __init__(self):
        #self.apt_id = None
        """db id fuck it pure ICAO PK"""
        self.icao = None
        """Airport code"""

        #self.is_icao = False 0 DEAD ;-))))))))
        """Is there airport a 4 letters apt ? == assume ICAO"""

        self.apt_name = None
        """Airport nice name"""

        self.apt_iata = None
        """Airport for passengers"""

        self.apt_type = None

        self.elevation_m = None
        """Airport elevation"""

        self.center = None
        """Center point"""
        self.beacon_id = 0
        """Beacon """
        self.services = 0
        """Airport services"""

        self.authority = 0
        self.apt_size = "small"


        self.apt_search = None
        """Search string"""

        self.closed = 0
        """Aiport closed"""

        self.runways = []

        self.points = []

        self.src_name = None
        self.src_src = None

    def dic(self):
        srr = "%s%s" % (self.apt_ident.upper(), self.apt_name.upper())
        srr = srr.replace(" ", "")
        return dict(
            #apt_id=self.apt_id,
            icao=self.icao,
            apt_iata=self.apt_iata,
            apt_name=self.apt_name,
            apt_type=self.apt_type,
            elevation_m=self.elevation_m,
            center=self.center,
            authority=self.authority,
            apt_size=self.apt_size,
            beacon_id=self.beacon_id,
            closed=self.closed,
            apt_search=srr,
            src_name=self.src_name,
            src_src=self.src_src
        )


class Rwy:
    """Representation of a runway for import purposes"""

    def __init__(self):
        self.apt_id = None
        """airport"""

        self.thr0 = None
        """Thr Object"""
        self.thr1 = None
        """Thr reciplical Object"""

        self.center = None
        """Center of runway"""

        self.length_m = None
        """length in metres (ft is created is view)"""
        self.width_m = None
        """width"""

        self.surface_id = None
        """Code for the surface type from runway_surface table"""

        self.shoulder_id = None
        """Code for the ??? TODO"""

        self.smoothness = None
        """Is this used ??"""

        self.center_lights = None
        """Runway has center lights"""

        self.edge_lights = None
        """Runway has edge lights"""

        self.auto_dist_signs = None
        """runway has distance markers ??"""

        self.src_name = None
        self.src_src = None

    def dic(self):
        return dict(
            apt_id=self.apt_id,
            thr0_id=self.thr0.thr_id,
            thr1_id=self.thr1.thr_id,
            center=self.center,
            width_m=self.width_m,
            length_m=self.length_m,
            shoulder_id=self.shoulder_id,
            surface_id=self.surface_id,
            smoothness=self.smoothness,
            center_lights=self.center_lights,
            edge_lights=self.edge_lights,
            auto_dist_signs=self.auto_dist_signs,
            src_name=self.src_name,
            src_src=self.src_src
        )


class Thr:
    """Representation of a threshold for import purposes"""

    def __init__(self):
        self.thr_id = None
        self.apt_id = None
        self.ident = None
        self.reciprocal = None

        self.lat = None
        self.lon = None

        self.dlat = None
        self.dlon = None
        self.displace = None

        self.overrun = None
        self.marking = None
        self.app_lights = None
        self.tdz_lights = None
        self.reil = None
        self.heading = None

        self.src_name = None
        self.src_src = None

    def dic(self):
        return dict(
            apt_id=self.apt_id,
            thr_ident=self.ident,
            reciprocal=self.reciprocal,
            thr_hdg=round(self.heading, 2),
            thr_start=ut.mk_point(lon=self.lon, lat=self.lat),
            thr_thr=ut.mk_point(lon=self.dlon, lat=self.dlat),
            thr_displaced=self.displace,
            thr_overrun=self.overrun,
            thr_marking=self.marking,
            thr_app_light_id=self.app_lights,
            thr_tdz_lights=self.tdz_lights,
            thr_reil=self.reil,
            src_name=self.src_name,
            src_src=self.src_src
        )


class Freq:
    """Import helper ATc at airport"""

    def __init__(self):
        self.apt_id = None
        self.type_id = None
        self.freq = None
        self.description = None
        self.range_nm = 50
        self.range_km = 92.6

    def dic(self):
        return dict(
            apt_id=self.apt_id,
            type_id=self.type_id,
            freq=self.freq,
            description=self.description,
            range_km=self.range_km,
            range_nm=self.range_nm
        )


"""				
count = 0

pointscollected = ""
runwaycount = 0
rwy_len_collect = []
apt_max_rwy_len_ft = 0
apt_min_rwy_len_ft = 0
apt_size = ""
lightingcollected = []
apt_ifr = "0"
apt_center_lon = ""
apt_center_lat = ""
apt_authority = ""
apt_services = ""
apt_country = ""
apt_name_utf8 = ""
apt_local_code = ""
bcn_type = ""
"""


def collecting(points, rwy_len, rwy_app_lighting):
    """
    # Collect runway points to insert airport center with ST_Centroid for all runway points,
    # collect runway length to insert min/max runway length (feet)
    TODO::
    """
    global pointscollected
    pointscollected += points

    global runwaycount
    runwaycount += 1

    global rwy_len_collect
    rwy_len_collect.append(rwy_len)

    # Check if there is an approach light and indicate if IFR is available or not
    # Needs to be discussed this one
    global lightingcollected
    lightingcollected += rwy_app_lighting


# print rwy_len_collect


def get_rwy_min_max(rwy_len_collect):
    """
        # Look for min/max runway length in rwy_len_collect
        # prepared for a more sophisticated list type
    """
    how_many_large_rwy = 0

    lenlist = zip(rwy_len_collect)

    print lenlist
    global apt_max_rwy_len_ft
    global apt_min_rwy_len_ft
    apt_max_rwy_len_ft = int(round(float(map(max, zip(*lenlist))[0]) * 3.048))
    apt_min_rwy_len_ft = int(round(float(map(min, zip(*lenlist))[0]) * 3.048))

    # Counting runways longer than 3200 meters / 9700 feet
    for i in rwy_len_collect:
        if int(float(i) * 3.048) >= 9700:
            how_many_large_rwy += 1

    # 2 runways >= 3200 meter = large
    # at least 1 runway >= 3200 meter = medium
    # rest = small
    global apt_size
    if how_many_large_rwy >= 2:
        apt_size = "large"
    elif how_many_large_rwy >= 1:
        apt_size = "medium"
    else:
        apt_size = "small"


def get_ifr(lightingcollected):
    global apt_ifr
    for i in lightingcollected:
        if i != "0":
            apt_ifr = "1"


def set_authority(apt):
    if apt.beacon_id == 4:
        apt.authority = "MIL"
    else:
        if apt.apt_name.startswith("[X]"):
            apt.authority = "CLO"
        else:
            apt.authority = "CIV"


def make_circle(rangerad, lon, lat):
    # We need 0 and 360 to close the polygon, see closepoly
    # What's a 'cricle' ? Should be sufficient to draw arc with 36 points.
    azi_list = range(0, 360, 10)
    circlelist = "POLYGON(("
    for i in azi_list:
        # Now be aware of this, geographiclib has lat/lon ordering, and not lon/lat
        result = Geodesic.WGS84.Direct(float(lat), float(lon), i, float(rangerad))
        # get it back in the right order
        circlelist += str(result["lon2"]) + " " + str(result["lat2"]) + ","

    # End point
    closepoly = Geodesic.WGS84.Direct(float(lat), float(lon), 0, float(rangerad))
    endpoint = str(closepoly["lon2"]) + " " + str(closepoly["lat2"])

    circlelist += endpoint + "))"
    #print circlelist
    return circlelist


def write_apt_circles(apt_ident):

    sql = "select apt_id, center_lat as lat,  center_lon as lon from v_airport "
    sql += " where apt_ident = %(apt_ident)s "
    db.Cur.execute(sql, dict(apt_ident=apt_ident))
    rows = db.Cur.fetchall()
    thr_id = None
    ident_lost = ""
    #if len(rows) == 0:
        ## Found a matching threshold from apt_dats
    row = rows[0]
    #print "APT=", row

   # circles30 = make_circle(55560, row['lon'], row['lat'])
    circles10 = make_circle(18520, row['lon'], row['lat'])
   #// thiscircles30 = circles30[:-2] + "))"
    thiscircles10 = circles10[:-2] + "))"
    #rangesql30 = "UPDATE airport SET apt_range_30nm=ST_Transform(ST_GeometryFromText('" + thiscircles30 + "', 4326),3857) WHERE apt_ident='" + apt_ident + "';"
    #db.Cur.execute(rangesql30)
    #db.Con.commit()
    rangesql10 = "UPDATE airport SET apt_range_10nm=ST_Transform(ST_GeometryFromText('" + thiscircles10 + "', 4326),3857) WHERE apt_ident='" +apt_ident + "';"
    db.Cur.execute(rangesql10)
    db.Con.commit()


def nuke_data():
    for t in ['threshold', 'runway', 'airport', "frequency", "sign"]:
        sql = "delete from %s;" % t
        db.Cur.execute(sql)
        db.Con.commit()


def insert_apt(**kwargs):
    """Insert to airport table and returns apt_id
        later processing in update_apt, eg center, range circle etc
    """
    sql = "insert into airport ( "
    sql += " icao, apt_name, apt_search, closed, apt_type, elevation_m, src_name, src_src, authority, apt_size "
    sql += ")values("
    sql += " %(icao)s, %(apt_name)s, %(apt_search)s, %(closed)s, %(apt_type)s, %(elevation_m)s, %(src_name)s, %(src_src)s, %(authority)s, %(apt_size)s "
    sql += ") returning icao;"
    #print sql
    try:
        db.Cur.execute(sql, kwargs)
    except Exception, e:
        print e
        print kwargs
        sys.exit(0)
    return db.Cur.fetchone()[0]


def update_apt(apt):
    """Process after the airport blob has been import and vars ready, eg center lat/lon"""
    dic = apt.dic()
    dic['multipoint'] = "MULTIPOINT(" + ",".join(apt.points) + ")"
    #print dic['multipoint']
    sql = "update airport set "
    sql += "beacon_id=%(beacon_id)s, authority=%(authority)s, closed=%(closed)s, "
    sql += " center=ST_Centroid(ST_Transform(ST_GeomFromText(%(multipoint)s, 4326),3857))"
    sql += " where apt_id=%(apt_id)s ;"
    try:
        db.Cur.execute(sql, dic)
    except Exception, e:
        print e
        print dic
        sys.exit(0)



def insert_rwy(**kwargs):
    """Insert to `runway` table and returns rwy_id"""
    sql = 'INSERT into runway ('

    sql += " apt_id, thr0_id, thr1_id, width_m, length_m, "
    sql += " surface_id, shoulder_id, smoothness,"
    sql += "center_lights, edge_lights, auto_dist_signs, "
    sql += " center, src_name, src_src "

    sql += ')values('

    sql += "%(apt_id)s, %(thr0_id)s, %(thr1_id)s, %(width_m)s, %(length_m)s, "
    sql += "%(surface_id)s,%(shoulder_id)s,%(smoothness)s,"
    sql += "%(center_lights)s,%(edge_lights)s,%(auto_dist_signs)s, "
    sql += " ST_Transform(ST_GeomFromText(%(center)s, 4326),3857), %(src_name)s, %(src_src)s  "

    sql += ") returning rwy_id; "
    #print kwargs
    try:
        db.Cur.execute(sql, kwargs)
    except Exception, e:
        print e
        print kwargs
        sys.exit(0)
    db.Con.commit()
    return db.Cur.fetchone()[0]


def insert_thr(**kwargs):
    """Inserts to the threshold table"""
    sqlt = "insert into threshold("

    sqlt += "apt_id, ident, hdg, reciprocal, start, threshold, displacement_m, "
    sqlt += "overrun, marking, app_light_id, tdz_lights, reil, src_name, src_src "

    sqlt += ")values("

    sqlt += " %(apt_id)s,  %(thr_ident)s, %(thr_hdg)s, %(reciprocal)s, "
    sqlt += " ST_Transform(ST_GeomFromText(%(thr_start)s, 4326),3857), "
    sqlt += " ST_Transform(ST_GeomFromText(%(thr_thr)s, 4326),3857), "
    sqlt += " %(thr_displaced)s, "
    sqlt += "%(thr_overrun)s, %(thr_marking)s, %(thr_app_light_id)s, %(thr_tdz_lights)s, %(thr_reil)s, %(src_name)s, %(src_src)s "

    sqlt += ") returning thr_id;"

    db.Cur.execute(sqlt, kwargs)
    db.Con.commit()
    return db.Cur.fetchone()[0]


def olde_insert_airport(apt_ident, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type):
    """The original function by gral"""
    global count

    slastcoma = len(pointscollected) - 1
    pointscollected2 = pointscollected[0:lastcoma]

    apt_center = "MULTIPOINT (" + pointscollected2 + ")"

    apt_rwy_count = runwaycount

    # Geometry is reprojected to EPSG:3857, should become a command line parameter
    sql = '''
		INSERT INTO airport (apt_ident, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type, apt_rwy_count, apt_min_rwy_len_ft, apt_max_rwy_len_ft, apt_size, apt_xplane_code, apt_ifr, apt_authority, apt_services, apt_center)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Centroid(ST_Transform(ST_GeomFromText(%s, 4326),3857)))'''

    params = [apt_ident, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type, apt_rwy_count, apt_min_rwy_len_ft,
              apt_max_rwy_len_ft, apt_size, apt_xplane_code, apt_ifr, apt_authority, apt_services, apt_center]
    db.Cur.execute(sql, params)

    db.Con.commit()


def insert_sign(apt_id, line):
    #print line
    #print "20   22.32152700  114.19750500 224.10  0 3 {@Y,^l}31-13{^r}"
    parts = ut.xsplit(line)
    point = ut.mk_point(lat=parts[1], lon=parts[2])
    params = dict(apt_id=apt_id,
                  center=point, orientation=parts[3],
                  size_id=parts[5], text=" ".join(parts[6:]))
    #print parts
    #print fii

    sql = "insert into sign("
    sql += "apt_id, text, size_id, orientation, point "
    sql += ")values("
    sql += " %(apt_id)s, %(text)s, %(size_id)s,%(orientation)s,  "
    sql += " ST_Transform(ST_GeomFromText(%(center)s, 4326),3857) "
    sql += ");"
    db.Cur.execute(sql, params)

    db.Con.commit()


def Olde_insert_runway(apt_ident, \
                       rwy_ident, \
                       rwy_ident_end, \
                       rwy_width, \
                       rwy_lon84, \
                       rwy_lat84, \
                       rwy_lon84_end, \
                       rwy_lat84_end, \
                       rwy_len_ft, \
                       rwy_len_m, \
                       rwy_hdg, \
                       rwy_hdg_end, \
                       rwy_surface, \
                       rwy_shoulder, \
                       rwy_smoothness, \
                       rwy_centerline_lights, \
                       rwy_edge_lighting, \
                       rwy_auto_dist_signs, \
                       rwy_threshold, \
                       rwy_threshold_lon, \
                       rwy_threshold_lat, \
                       rwy_overrun, \
                       rwy_marking, \
                       rwy_app_lighting, \
                       rwy_tdz_lighting, \
                       rwy_reil, \
                       rwy_threshold_end, \
                       rwy_threshold_lon_end, \
                       rwy_threshold_lat_end, \
                       rwy_overrun_end, \
                       rwy_marking_end, \
                       rwy_app_lighting_end, \
                       rwy_tdz_lighting_end, \
                       rwy_reil_end, \
                       rwy_xplane_code, \
                       A_lat, A_lon, B_lat, B_lon, C_lat, C_lon, D_lat, D_lon):
    """Origin gral function.. still need to implement parts"""

    # Coordinate ordering is (x, y) -- that is (lon, lat)
    # Polygon needs to be closed, repeating starting point
    rwy_poly = "POLYGON (( " + str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(
        C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + "," + str(A_lon) + " " + str(A_lat) + " ))"
    #print rwy_polygon

    rwy_center = "POINT(" + str(rwy_lon84) + " " + str(rwy_lat84) + ")"
    rwy_center_end = "POINT(" + str(rwy_lon84_end) + " " + str(rwy_lat84_end) + ")"

    rwy_threshold_center = "POINT(" + str(rwy_threshold_lon) + " " + str(rwy_threshold_lat) + ")"
    rwy_threshold_center_end = "POINT(" + str(rwy_threshold_lon_end) + " " + str(rwy_threshold_lat_end) + ")"

    # Geometry is reprojected to EPSG:3857
    rwy_appFT_2_M_lighting = None
    sql = '''
		INSERT INTO runway (apt_ident, rwy_ident, rwy_ident_end, rwy_width, rwy_lon84, rwy_lat84, rwy_lon84_end, rwy_lat84_end, rwy_len_ft, rwy_len_m, rwy_hdg, rwy_hdg_end, rwy_surface,rwy_shoulder,rwy_smoothness,rwy_centerline_lights,rwy_edge_lighting,rwy_auto_dist_signs,rwy_threshold,rwy_overrun,rwy_marking,rwy_app_lighting,rwy_tdz_lighting,rwy_reil,rwy_threshold_end,rwy_overrun_end,rwy_marking_end,rwy_app_lighting_end,rwy_tdz_lighting_end,rwy_reil_end, rwy_xplane_code, rwy_poly, rwy_center, rwy_center_end, rwy_threshold_center, rwy_threshold_center_end)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Transform(ST_GeomFromText(%s, 4326),3857),ST_Transform(ST_GeomFromText(%s, 4326),3857),ST_Transform(ST_GeomFromText(%s, 4326),3857),ST_Transform(ST_GeomFromText(%s, 4326),3857),ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
    params = [apt_ident, rwy_ident, rwy_ident_end, rwy_width, rwy_lon84, rwy_lat84, rwy_lon84_end, rwy_lat84_end,
              rwy_len_ft, rwy_len_m, rwy_hdg, rwy_hdg_end, rwy_surface, rwy_shoulder, rwy_smoothness,
              rwy_centerline_lights, rwy_edge_lighting, rwy_auto_dist_signs, rwy_threshold, rwy_overrun, rwy_marking,
              rwy_appFT_2_M_lighting, rwy_tdz_lighting, rwy_reil, rwy_threshold_end, rwy_overrun_end, rwy_marking_end,
              rwy_app_lighting_end, rwy_tdz_lighting_end, rwy_reil_end, rwy_xplane_code, rwy_poly, rwy_center,
              rwy_center_end, rwy_threshold_center, rwy_threshold_center_end]

    db.Cur.execute(sql, params)

    points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(
        C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","


# query gives lon/lat (postgis x/y) as text for the center point in reprojected format
#sql2 = "UPDATE runway SET rwy_center_lon=ST_X(rwy_center), rwy_center_lat=ST_Y(rwy_center),rwy_center_lon_end=ST_X(rwy_center), rwy_center_lat_end=ST_Y(rwy_center),rwy_threshold_lon=ST_X(rwy_threshold_center), rwy_threshold_lat=ST_Y(rwy_threshold_center),rwy_threshold_lon_end=ST_X(rwy_threshold_center_end), rwy_threshold_lat_end=ST_Y(rwy_threshold_center_end) WHERE rwy_ident='"+rwy_ident+"';"
#cur.execute(sql2)




def insert_waterway(apt_ident, \
                    wwy_ident, \
                    wwy_ident_end, \
                    wwy_width, \
                    wwy_lon, \
                    wwy_lat, \
                    wwy_lon_end, \
                    wwy_lat_end, \
                    wwy_len_ft, \
                    wwy_len_m, \
                    wwy_hdg, \
                    wwy_hdg_end, \
                    wwy_buoys, \
                    wwy_xplane_code, \
                    A_lat, A_lon, B_lat, B_lon, C_lat, C_lon, D_lat, D_lon):
    """TODO original gral stuff.. TO BE reimplemented.. ignored for now"""
    # Coordinate ordering is (x, y) -- that is (lon, lat)
    # Polygon needs to be closed, repeating starting point
    wwy_poly = "POLYGON (( " + str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(
        C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + "," + str(A_lon) + " " + str(A_lat) + " ))"
    #print wwy_polygon

    # Geometry is reprojected to EPSG:3857
    sql = '''
		INSERT INTO waterway (apt_ident, wwy_ident, wwy_ident_end, wwy_width, wwy_lon, wwy_lat, wwy_lon_end, wwy_lat_end, wwy_len_ft, wwy_len_m, wwy_hdg, wwy_hdg_end, wwy_buoys, wwy_xplane_code, wwy_poly)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
    params = [apt_ident, wwy_ident, wwy_ident_end, wwy_width, wwy_lon, wwy_lat, wwy_lon_end, wwy_lat_end, wwy_len_ft,
              wwy_len_m, wwy_hdg, wwy_hdg_end, wwy_buoys, wwy_xplane_code, wwy_poly]
    db.Cur.execute(sql, params)

    points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(
        C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","


def insert_helipad(apt_ident, \
                   pad_ident, \
                   pad_lon, \
                   pad_lat, \
                   pad_lon_end, \
                   pad_lat_end, \
                   pad_hdg, \
                   pad_hdg_end, \
                   pad_len_m, \
                   pad_len_ft, \
                   pad_width_m, \
                   pad_width_ft, \
                   pad_surface, \
                   pad_marking, \
                   pad_shoulder, \
                   pad_edge_lighting, \
                   pad_app_lighting, \
                   pad_xplane_code, \
                   A_lat, A_lon, B_lat, B_lon, C_lat, C_lon, D_lat, D_lon):
    """original gral stuff.. TO BE reimplemented.. ignored for now"""

    # Coordinate ordering is (x, y) -- that is (lon, lat)
    # Polygon needs to be closed, repeating starting point
    pad_poly = "POLYGON (( " + str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(
        C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + "," + str(A_lon) + " " + str(A_lat) + " ))"
    #print wwy_polygon

    # Geometry is reprojected to EPSG:3857
    sql = '''
		INSERT INTO helipad (apt_ident, pad_ident, pad_lon, pad_lat, pad_lon_end, pad_lat_end, pad_hdg, pad_hdg_end, pad_len_m, pad_len_ft, pad_width_m, pad_width_ft, pad_surface, pad_marking, pad_shoulder, pad_edge_lighting, pad_app_lighting, pad_xplane_code, pad_poly)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
    params = [apt_ident, pad_ident, pad_lon, pad_lat, pad_lon_end, pad_lat_end, pad_hdg, pad_hdg_end, pad_len_m,
              pad_len_ft, pad_width_m, pad_width_ft, pad_surface, pad_marking, pad_shoulder, pad_edge_lighting,
              pad_app_lighting, pad_xplane_code, pad_poly]
    db.Cur.execute(sql, params)

    points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(
        C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","


##================================================================
def insert_freq(apt_id, line):
    """Insert an ATC freq from line"""
    f = Freq()
    f.apt_id = apt_id
    f.type_id = int(line[0:2])
    f.freq = int(line[3:8]) / 100
    f.description = line[9:]

    sql = "INSERT INTO frequency ("
    sql += "apt_id, type_id, freq_mhz, description, range_km, range_nm "
    sql += ")VALUES ("
    sql += "%(apt_id)s, %(type_id)s, %(freq)s, %(description)s, %(range_km)s, %(range_nm)s "
    sql += ");"
    db.Cur.execute(sql, f.dic())


def get_apt_dir(code):
    return "/" + code[0] + "/" + code[1] + "/" + code[2]


def shard(dir_path=None, src_name=None):
    """Import file 'apt.dat."""
    nuke_data()


    xrec = conf.get_current()
    dir_path = conf.work_dir("/xplane_unzipped/%s" % xrec['zip_dir'])

    reader = open(dir_path + "/apt.dat", 'r')

    reader.next()
    reader.next()
    reader.next()
    reader.next()

    print "First 4 lines of apt.dat skipped."

    xindex = []
    apt_ident = ""
    xlines = []
    c = 4
    for line in reader:
        #print "=", c, line[0:10]
        ## strip line
        lin = line.strip()

        if len(lin) > 0:
            ## Its not a blank line so append
            xlines.append(lin)

        else:

            apt_ident, ok = write_data_shard(xlines, xrec)
           # print apt_ident
            if ok:
                xindex.append(apt_ident)
            ##file_path = ws_path = ""
            ##fn = open()  ## Its a blank line so process xlines
            #apt, err = process_apt(xlines, src_name)
            #print "process=", apt, err
            #if err == QUIRK:
            #	pass
            #else:
            #	if apt != None:
            #		update_apt(apt)
            xlines = []
        if c % 1000 == 0:
            print c, apt_ident if ok else "%s - skip" % apt_ident
        c += 1

    file_path = conf.work_dir( "/raw_data/apt/index.%s.json" % xrec['date'] )
    conf.write_json(file_path, dict(airports=sorted(xindex), count=len(xindex)) )


def write_data_shard(xlines, xrec):

    parts = xlines[0].split(" ")

    if parts[0] == "1":  ## apt only
        apt_ident = xlines[0][15:19].strip()
        if apt_ident in ["NZSP", "EDRZ", "UBAK"]:
            print "BANNED >>>>>>>>>>>>>> ", apt_ident
            return None, False

        if ut.is_icao(apt_ident):
            dir_path = conf.work_dir("/raw_data/apt")
            dir_path += get_apt_dir(apt_ident)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            file_path = dir_path + "/%s.%s.dat" % (apt_ident, xrec['date'])
            #print file_path
            f = open(file_path, "w")
            f.write("\n".join(xlines))
            f.close()
            return apt_ident, True

        return apt_ident, False
    return None, False


def import_airports(apt_ident=None):

    nuke_data()

    xrec = conf.get_current()
    xdate = xrec['date']

    if apt_ident:
        import_airport(apt_ident, xrec)
        return


    idx_file = conf.work_dir("/raw_data/apt/index.%s.json" % xrec['date'])
    data = conf.read_json(idx_file)

    print "processing - %s" % data['count']
    for c, apt_ident in enumerate(data['airports']):
        import_airport(apt_ident, xrec)
        if c % 100 == 0:
            print "%s of %s\t%s" % (c, data['count'], apt_ident)

def import_airport(apt_ident, xrec=None):
    apt_file = conf.work_dir("/raw_data/apt/")
    apt_file += get_apt_dir(apt_ident)
    apt_file += "/%s.%s.dat" % ( apt_ident, xrec['date'])
    f = open(apt_file, "r")
    s = f.read()
    f.close()
    xlines = s.split("\n")
    process_apt(apt_ident, xlines, xrec)




def process_apt(apt_ident, xlines, xrec):
    """Process a `list` of lines comprising and airport block

    Returns: an Apt class with all the bits
    """
    #print xlines[0]
    #return


    #apt_id = None
    apt = None

    ## skip sealport, heliport for now
    apt_codes = [1]  # , 16, 17]

    ##idiot check first line is an apt code
    ll = int(xlines[0].split(" ")[0])
    if ll == 1200:
        print "STRANGE quirk"
        return None, QUIRK

    #if not ll in apt_codes:
    #    print "panic", xlines[0]
    #PANIC
    src_name = "xplane-%s" % xrec['date']
    for uline in xlines:


        #print uline
        line = ut.safe_str(uline)
        parts = line.split(" ")
        row_code = int(parts[0])

        if row_code in [1]:

            """
            sql = 'select src_name, src_src from airport where apt_ident=%(apt_ident)s; '
            db.Cur.execute(sql, dict(apt_ident=apt_ident))
            rows = db.Cur.fetchall()
            ##thr_id = None
            ##i#dent_lost = ""
            if len(rows) > 0:
                ## Found a matching threshold from apt_dats
                row = rows[0]
                print rows
                print "found", row

                if row['src_src'] == line:
                    print "matched"
            """
            apt = Apt()
            apt.apt_ident = apt_ident
            apt.src_name = src_name
            apt.src_src = line

            #print apt.apt_ident, apt.is_icao
            apt_name = line[20:].strip()
            if apt_name.startswith("[X]"):
                apt_name = apt_name.replace("[X]", "").strip()
                apt_name = apt_name.replace("CLOSED", "").strip()
                apt.closed = 1

            apt.apt_name = apt_name

            apt.elevation_m = int(float(line[4:10]) * FT_2_M)
            apt.apt_type = "land"

            if row_code == 16:
                apt.apt_type = "seaport"

            elif row_code == 17:
                apt.apt_type = "heliport"

            apt.authority = 0
            apt.apt_id = insert_apt(**apt.dic())


        #print "apt_id=", apt.apt_id, apt.apt_ident,  apt.is_icao


        # runways, we need it for some calculation, i.e. centerpoint
        # but also for getting shortest/longest runway, to set the apt_ifr
        # flag and much more
        if row_code == 100:
            ## create Rwy object
            rwy = Rwy()
            rwy.apt_id = apt.apt_id
            rwy.width_m = line[5:13].strip()
            rwy.surface_id = line[14:16].replace(" ", "").strip()
            rwy.shoulder_id = line[17:19].replace(" ", "").strip()
            rwy.smoothness = line[20:24].strip()
            rwy.center_lights = line[25].strip()
            rwy.edge_lights = line[27].strip()
            rwy.auto_dist_signs = line[29].strip()
            rwy.src_name = src_name
            rwy.src_src = line

            if rwy.surface_id:
                if rwy.surface_id == "1" or rwy.surface_id == "2":
                    apt.apt_size = "small"
                #print ">", rwy.surface_id, type(rwy.surface_id)

            # threshold 0
            rwy.thr0 = Thr()
            rwy.thr0.apt_id = apt.apt_id
            rwy.thr0.ident = str(line[31:34]).strip(" ")
            rwy.thr0.lat = line[34:47]
            rwy.thr0.lon = line[48:61]
            rwy.thr0.displace = line[62:69].strip()
            rwy.thr0.overrun = line[70:77].strip()
            rwy.thr0.marking = line[78:79].strip()
            rwy.thr0.app_lights = line[81:82].strip()
            rwy.thr0.tdz_lights = line[83].strip()
            rwy.thr0.reil = line[85].strip()
            rwy.thr0.src_name = src_name
            rwy.thr0.src_src = line

            # threshold 1
            #rwy_number_end = str(line[87:90])
            rwy.thr1 = Thr()
            rwy.thr1.apt_id = apt.apt_id
            rwy.thr1.ident = str(line[87:90]).strip(" ")
            rwy.thr1.lat = line[90:103]
            rwy.thr1.lon = line[104:117]
            rwy.thr1.displace = line[119:125].strip()
            rwy.thr1.overrun = line[126:133].strip()
            rwy.thr1.marking = line[134:135].strip()
            rwy.thr1.app_lights = line[136:138].replace(" ", "").strip()
            rwy.thr1.tdz_lights = line[139].strip()
            rwy.thr1.reil = line[141].strip()
            rwy.thr1.src_name = src_name
            rwy.thr1.src_src = line

            rwy.thr0.reciprocal = rwy.thr1.ident
            rwy.thr1.reciprocal = rwy.thr0.ident



            ## Set the threshold and wunawy params

            set_runway_hdg_length(rwy, line)

            rwy.thr0.thr_id = insert_thr(**rwy.thr0.dic())
            rwy.thr1.thr_id = insert_thr(**rwy.thr1.dic())


            # Calculating runway points
            ## TODO
            apt.points.append("%s %s" % (rwy.thr0.lon, rwy.thr0.lat))
            apt.points.append("%s %s" % (rwy.thr1.lon, rwy.thr1.lat))

            ## Set opposite ident
            sql = 'update threshold set recip_id =%(recip_id)s where thr_id = %(thr_id)s'
            db.Cur.execute(sql, dict(recip_id=rwy.thr1.thr_id, thr_id=rwy.thr0.thr_id))
            db.Cur.execute(sql, dict(recip_id=rwy.thr0.thr_id, thr_id=rwy.thr1.thr_id))



            ### Insert the runway
            rwy_id = insert_rwy(**rwy.dic())

        ## Airport sign
        if row_code == 20:
            #insert_sign(apt.apt_id, line)
            pass


        # WATER runways TODO
        if False and row_code == 101:
            # #Water Runways
            wwy = Rwy()
            wwy.width_m = line[4:11].strip()
            wwy_buoys = line[12:13].strip()

            th0 = Thr()
            th0.ident = str(line[14:16])
            th0.lat = line[17:31]
            th0.lon = line[32:45]

            th1 = Thr()
            th1.ident = str(line[46:48])
            th1.lat = line[49:62]
            th1.lon = line[63:79]

            wwy_app_lighting = "0"

            # Now some additional data, not in apt.dat
            set_runway_hdg_length(rwy, th0, th1)
            #wwy_lenc = Geodesic.WGS84.Inverse(float(th0.lat), float(th0.lon), float(th1.lat), float(th1.lon))
            #rwy.length_m = str(wwy_len.get("s12"))

            #print "Meters: "+wwy_len_m

            #wwy_len_ft = wwy_len.get("s12")*3.048

            #thr0.heading = wwy_lenc.get("azi2")

            #wwy_lenc_end = Geodesic.WGS84.Inverse(float(th1.lat), float(th1.lon), float(th0.lat), float(th0.lon))
            #thr1.heading = str(360.0 + wwy_len_end.get("azi2"))

            # Calculating runway points
            wwy_direct_A = Geodesic.WGS84.Direct(float(wwy_lat), float(wwy_lon), float(wwy_hdg - 90.0),
                                                 (float(wwy_width)) / 2)
            A_lat = wwy_direct_A.get("lat2")
            A_lon = wwy_direct_A.get("lon2")

            wwy_direct_B = Geodesic.WGS84.Direct(float(wwy_lat), float(wwy_lon), float(wwy_hdg + 90.0),
                                                 (float(wwy_width)) / 2)
            B_lat = wwy_direct_B.get("lat2")
            B_lon = wwy_direct_B.get("lon2")

            wwy_direct_C = Geodesic.WGS84.Direct(float(wwy_lat_end), float(wwy_lon_end),
                                                 -360.0 + float(wwy_hdg_end) - 90.0, (float(wwy_width)) / 2)
            C_lat = wwy_direct_C.get("lat2")
            C_lon = wwy_direct_C.get("lon2")

            wwy_direct_D = Geodesic.WGS84.Direct(float(wwy_lat_end), float(wwy_lon_end),
                                                 -360.0 + float(wwy_hdg_end) + 90.0, (float(wwy_width)) / 2)
            D_lat = wwy_direct_D.get("lat2")
            D_lon = wwy_direct_D.get("lon2")

            # Collecting runway points
            points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(
                C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","
            collecting(points, wwy_len_m, wwy_app_lighting)

            ##insert_www(**)
            insert_waterway(apt_ident, wwy_ident, wwy_ident_end, wwy_width, wwy_lon, wwy_lat, wwy_lon_end, wwy_lat_end,
                            wwy_len_m, wwy_len_ft, wwy_hdg, wwy_hdg_end, wwy_buoys, wwy_xplane_code, \
                            A_lat, A_lon, B_lat, B_lon, C_lat, C_lon, D_lat, D_lon)

        # HELIPADS, we need it for heliport calculation, i.e. centerpoint
        # but we dont want to take this points into account for regular airports
        # so we look out for (H)
        if False and row_code == 102:

            pad_xplane_code = line[0:3]
            pad_ident = str(line[4:6])
            pad_lat_read = line[7:19]
            pad_lon_read = line[21:33]
            pad_hdg = line[34:41]
            pad_len_m = line[42:49]
            pad_width_m = line[50:57]
            pad_surface = line[58:61]
            pad_marking = line[61:63]
            pad_shoulder = line[65:67]
            pad_smoothness = line[68:72]
            pad_edge_lighting = line[73]

            pad_app_lighting = "0"

            # Now some additional data, not in apt.dat

            # We get the centerpoint of the pad, but we want the center point at shape start,
            # to get it calculated like runways and to prevent me from writing all separated for pads
            pad_direct = Geodesic.WGS84.Direct(float(pad_lat_read), float(pad_lon_read), float(pad_hdg) - 180.0,
                                               (float(pad_len_m)) / 2)
            pad_lat = pad_direct.get("lat2")
            pad_lon = pad_direct.get("lon2")

            pad_direct_end = Geodesic.WGS84.Direct(float(pad_lat_read), float(pad_lon_read), float(pad_hdg),
                                                   (float(pad_len_m)))
            pad_lat_end = pad_direct_end.get("lat2")
            pad_lon_end = pad_direct_end.get("lon2")

            pad_len = Geodesic.WGS84.Inverse(float(pad_lat), float(pad_lon), float(pad_lat_end), float(pad_lon_end))
            pad_len_m = str(pad_len.get("s12"))

            #print "Meters: "+pad_len_m

            pad_len_ft = float(pad_len_m) * 3.048
            pad_width_ft = float(pad_width_m) * 3.048

            pad_hdg = pad_len.get("azi2")

            pad_len_end = Geodesic.WGS84.Inverse(float(pad_lat_end), float(pad_lon_end), float(pad_lat), float(pad_lon))
            pad_hdg_end = str(360.0 + pad_len_end.get("azi2"))

            # Calculating runway points
            pad_direct_A = Geodesic.WGS84.Direct(float(pad_lat), float(pad_lon), float(pad_hdg - 90.0),
                                                 (float(pad_width_m)) / 2)
            A_lat = pad_direct_A.get("lat2")
            A_lon = pad_direct_A.get("lon2")

            pad_direct_B = Geodesic.WGS84.Direct(float(pad_lat), float(pad_lon), float(pad_hdg + 90.0),
                                                 (float(pad_width_m)) / 2)
            B_lat = pad_direct_B.get("lat2")
            B_lon = pad_direct_B.get("lon2")

            pad_direct_C = Geodesic.WGS84.Direct(float(pad_lat_end), float(pad_lon_end),
                                                 -360.0 + float(pad_hdg_end) - 90.0, (float(pad_width_m)) / 2)
            C_lat = pad_direct_C.get("lat2")
            C_lon = pad_direct_C.get("lon2")

            pad_direct_D = Geodesic.WGS84.Direct(float(pad_lat_end), float(pad_lon_end),
                                                 -360.0 + float(pad_hdg_end) + 90.0, (float(pad_width_m)) / 2)
            D_lat = pad_direct_D.get("lat2")
            D_lon = pad_direct_D.get("lon2")

            # Collecting runway points
            points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(
                C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","

            # We only collect for the heliports, there we need the points for the center, NOT for the airports
            if apt_name_ascii.startswith("[H]"):
                collecting(points, pad_len_m, pad_app_lighting)

            insert_helipad(apt_ident, pad_ident, pad_lon, pad_lat, pad_lon_end, pad_lat_end, pad_hdg, pad_hdg_end,
                           pad_len_m, pad_len_ft, pad_width_m, pad_width_ft, pad_surface, pad_marking, pad_shoulder,
                           pad_edge_lighting, pad_app_lighting, pad_xplane_code, \
                           A_lat, A_lon, B_lat, B_lon, C_lat, C_lon, D_lat, D_lon)


        # ATC frequencies
        # Calculating range later ?
        # NM factor = 1.852
        # Standard range = 50 nm = 92,6 km
        if row_code >= 50 and row_code <= 56:
            insert_freq(apt.apt_id, line)

        ## Beacon
        # One green and two white flashes means military airport - no civil aircraft allowed.
        # xplane data beacon type code 4: military
        #global bcn_type
        if row_code == 18:
            apt.beacon_id = line[31:32].strip()

        # When there is a tower frequency, there are services probably
        if row_code == 54:  #line.startswith("54 "):
            apt.services = 1

        #print line
    update_apt(apt)
    write_apt_circles(apt.apt_ident)
    return apt, None


def set_runway_hdg_length(rwy, line=None):
    """Caclulates and sets the threshold offset lines, threshold heading, disatance"""

    t0 = rwy.thr0
    t1 = rwy.thr1

    ## We calculate the runway length as distance between two thresholds
    ## but does this allow for displacements ??
    # maybe it should all be metres in db and convert on the fly
    rwy_calc = Geodesic.WGS84.Inverse(float(t0.lat), float(t0.lon), float(t1.lat), float(t1.lon))
    rwy.length_m = rwy_calc.get("s12")
    #rwy_len_ft = rwy_calc.get("s12") * 3.048
    ## the heading for this end
    t0.heading = rwy_calc.get("azi2")
    if t0.heading < 0:
        t0.heading = rwy_calc.get("azi2") + 360
        """
        print "=", t0.ident, rwy_calc.get("azi1"),  rwy_calc.get("azi2")
        print line
        print float(t0.lat), float(t0.lon), float(t1.lat), float(t1.lon)
        print "?", t0.ident, rwy_calc.get("azi2") + 360
        print
        """
    # Calculate the heading for other end
    rwy_length_end = Geodesic.WGS84.Inverse(float(t1.lat), float(t1.lon), float(t0.lat), float(t0.lon))
    t1.heading = 360.0 + rwy_length_end.get("azi2")


    ## Caclulate the point for the threhold.. = start point, heading and distance in m
    rwy_threshold_direct = Geodesic.WGS84.Direct(float(t0.lat), float(t0.lon), float(t0.heading), float(t0.displace))
    t0.dlon = str(rwy_threshold_direct["lon2"])
    t0.dlat = str(rwy_threshold_direct["lat2"])

    rwy_threshold_direct_end = Geodesic.WGS84.Direct(float(t1.lat), float(t1.lon), rwy_length_end.get("azi2"),
                                                     float(t1.displace))
    t1.dlon = str(rwy_threshold_direct_end["lon2"])
    t1.dlat = str(rwy_threshold_direct_end["lat2"])

    ## pete hack to calculate runwaycenter
    rwy_middle = Geodesic.WGS84.Direct(float(t0.lat), float(t0.lon), float(t0.heading), float(rwy.length_m / 2))
    # umm maybe we need to calc middle of displaced	??
    rwy.center = ut.mk_point(lat=str(rwy_middle["lat2"]), lon=str(rwy_middle["lon2"]))


    #if t1.heading > 360:
    #    t1.heading = t1.heading - 360


    if t0.heading > 360.00:
        t0.heading = t0.heading - 360.00
    if t1.heading > 360.00:
        t1.heading = t1.heading - 360.00

if __name__ == "__main__":
    apt_dat_path = sys.argv[1]

    import_apt_dat(apt_dat_path)

    # The parser has some tolerance with wrong newlines, but we
    # need to remove duplicates produced with tolerance.
    # This is not that dangerous, because the apt_ident should
    # be unique anyway ...

    cur.execute(
        "DELETE FROM airport WHERE apt_id NOT IN (SELECT MAX(dup.apt_id) FROM airport As dup GROUP BY dup.apt_ident);")
    print "Removing duplicates in airports table ..."
    log.write("Duplicates removed.\n")
    conn.commit()

    # Doing geometry updates in airports
    sqlapt = "SELECT * from airport"
    cur.execute(sqlapt)
    allapt = cur.fetchall()
    conn.commit()

    countapt = 0
    countcircle = 0

    print "Updating coords in airport ..."

    for rowapt1 in allapt:
        # query gives lon/lat (postgis x/y) as text for the center point in reprojected format
        sql2 = "UPDATE airport SET apt_center_lon=ST_X(apt_center), apt_center_lat=ST_Y(apt_center) WHERE apt_ident='" + \
               rowapt1[1] + "';"
        cur.execute(sql2)
        conn.commit()

        # query gives lon/lat (postgis x/y) as text for the center point in WGS84 format
        sql3 = "UPDATE airport SET apt_center_lon84=ST_X(ST_Transform(apt_center,4326)), apt_center_lat84=ST_Y(ST_Transform(apt_center,4326)) WHERE apt_ident='" + \
               rowapt1[1] + "';"
        cur.execute(sql3)
        conn.commit()

        countapt += 1
        print "Updated airport with human readable coords: " + rowapt1[1] + " " + str(countapt)

    print "Drawing range circle airports ..."

    for rowapt in allapt:
        latsql = "SELECT apt_center_lat84,apt_center_lon84 FROM airport WHERE apt_ident='" + rowapt[1] + "';"
        cur.execute(latsql)

        latlon = cur.fetchall()[0]
        lat84 = latlon[0]
        lon84 = latlon[1]

        # Drawing the range polygons

        # For more ranges once could use this iter below, for two it's ok to have it
        # without I guess, like below-below

        #listcircles = [55560,18520] # 30/10 nautic miles

        #for i in listcircles:
        #	circles = drawcircle(i,lon84,lat84)
        #	thiscircles = circles[:-2]+"))"
        #	rangesql = "UPDATE airport SET apt_range=ST_Transform(ST_GeometryFromText('"+thiscircles+"', 4326),3857) WHERE apt_ident='"+apt_ident+"';"
        #	cur.execute(rangesql)

        circles30 = drawcircle(55560, lon84, lat84)
        circles10 = drawcircle(18520, lon84, lat84)
        thiscircles30 = circles30[:-2] + "))"
        thiscircles10 = circles10[:-2] + "))"
        rangesql30 = "UPDATE airport SET apt_range_30nm=ST_Transform(ST_GeometryFromText('" + thiscircles30 + "', 4326),3857) WHERE apt_ident='" + \
                     rowapt[1] + "';"
        cur.execute(rangesql30)
        conn.commit()
        rangesql10 = "UPDATE airport SET apt_range_10nm=ST_Transform(ST_GeometryFromText('" + thiscircles10 + "', 4326),3857) WHERE apt_ident='" + \
                     rowapt[1] + "';"
        cur.execute(rangesql10)
        conn.commit()

        countcircle += 1
        print "Drawing circles for airport range: " + str(rowapt[1]) + " " + str(countcircle)

    print "Updating runways with coords ..."

# Doing geometry updates in runways
#sqlrwy = "SELECT * from runway"
#cur.execute(sqlrwy)
#allrwy = cur.fetchall()
#conn.commit()

#countrwy = 0

#for rowrwy in allrwy: 
# query gives lon/lat (postgis x/y) as text for the center point in reprojected format
#sqlrwy1 = "UPDATE runway SET rwy_center_lon=ST_X(rwy_center),rwy_center_lat=ST_Y(rwy_center) WHERE rwy_ident='"+rowrwy[2]+"';"
#sqlrwy2 = "UPDATE runway SET rwy_center_lon_end=ST_X(rwy_center_end),rwy_center_lat_end=ST_Y(rwy_center_end) WHERE rwy_ident='"+rowrwy[2]+"';"
#sqlrwy3 = "UPDATE runway SET rwy_threshold_lon=ST_X(rwy_threshold_center),rwy_threshold_lat=ST_Y(rwy_threshold_center) WHERE rwy_ident='"+rowrwy[2]+"';"
#sqlrwy4 = "UPDATE runway SET rwy_threshold_lon_end=ST_X(rwy_threshold_center_end),rwy_threshold_lat_end=ST_Y(rwy_threshold_center_end) WHERE rwy_ident='"+rowrwy[2]+"';"

#cur.execute(sqlrwy1)
#conn.commit()

#cur.execute(sqlrwy2)
#conn.commit()

#cur.execute(sqlrwy3)
#conn.commit()

#cur.execute(sqlrwy4)
#conn.commit()

#countrwy += 1
#print "Updated runway of airport: "+str(rowrwy[1])+" "+str(countrwy)



