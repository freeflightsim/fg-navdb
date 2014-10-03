#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#
# Better remove the bad design with the globals instead. Thanks.

import sys

# geographiclib 1.24 by (c) Charles Karney
from geographiclib.geodesic import Geodesic

from navimport import conf
from navimport import db
from navimport import utils as ut

NM_2_M = 1852

DATA_FILE_NAME = "/earth_nav.dat"


class RC:
    """Row Codes used in earth_nav.dat"""

    ndb = 2
    """NDB (Non-Directional Beacon)- Includes NDB component of Locator Outer Markers (LOM)"""

    vor = 3

    loc_ils1 = 4
    loc_ils2 = 5

    gs = 6

    om = 7
    mm = 8
    im = 9

    dme_ils = 12
    dme = 13

    @staticmethod
    def list():
        return [
            RC.ndb, RC.vor, RC.dme_ils, RC.dme,
            RC.loc_ils1, RC.loc_ils2, RC.gs,
            RC.mm, RC.om, RC.im
        ]

    @staticmethod
    def ntype(row_code):
        id = int(row_code)
        if id  == 2:
            return "ndb"

        if id  == 3:
            return "vor"

        if id  == 4:
            return "ils"

        if id  == 5:
            return "ils-2"

        if id  == 6:
            return "gs"

        if id  == 7:
            return "om"
        if id  == 8:
            return "mm"
        if id  == 9:
            return "im"

        if id == 12:
            return "dme_ils"
        if id == 13:
            return "dme"

        return "UNK"


entrycount = 0


def drawcircle(rangerad, lon, lat):
    """TODO or can this be dynamic in view"""
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
    return circlelist


# class Ob:


def insert_navaid_olde(nav_ident,
                       apt_ident, \
                       rwy_ident, \
                       nav_elev_ft, \
                       nav_freq_khz, \
                       nav_freq_mhz, \
                       nav_bearing_true, \
                       nav_var_deg, \
                       nav_name, \
                       nav_suffix, \
                       nav_center_lon84, \
                       nav_center_lat84, \
                       nav_range_nm, \
                       nav_bias_nm, \
                       nav_standalone, \
                       nav_no_freq, \
                       nav_xplane_code):
    nav_center = "POINT(" + nav_center_lon84 + " " + nav_center_lat84 + ")"

    params = dict(
        nav_ident=nav_ident,
        apt_ident=apt_ident,
        rwy_ident=rwy_ident,
        nav_elev_ft=nav_elev_ft,
        nav_freq_khz=nav_freq_khz,
        nav_freq_mhz=nav_freq_mhz,
        nav_bearing_true=nav_bearing_true,
        nav_var_deg=nav_var_deg,
        nav_name=nav_name,
        nav_suffix=nav_suffix,
        nav_center_lon84=nav_center_lon84,
        nav_center_lat84=nav_center_lat84,
        nav_range_nm=nav_range_nm,
        nav_bias_nm=nav_bias_nm,
        nav_standalone=nav_standalone,
        nav_no_freq=nav_no_freq,
        nav_xplane_code=nav_xplane_code,
        nav_center=nav_center
    )
    '''nav_ident,apt_ident,rwy_ident,nav_elev_ft,nav_freq_khz,nav_freq_mhz,nav_bearing_true,nav_var_deg,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,nav_bias_nm,nav_standalone,nav_no_freq,nav_xplane_code'''
    '''separated: nav_center,nav_center_lon,nav_center_lat,nav_range_poly'''

    sql = "insert into navaid ("

    sql += "nav_ident,apt_ident,rwy_ident,nav_elev_ft, "
    sql += "nav_freq_khz,nav_freq_mhz,nav_bearing_true,nav_var_deg,"
    sql += "nav_name, nav_suffix,"
    #sql += "nav_center_lon84,nav_center_lat84,"
    sql += "nav_range_nm,nav_bias_nm,nav_standalone,nav_no_freq,nav_xplane_code,"
    sql += "nav_center "

    sql += ")VALUES ("

    sql += "%(nav_ident)s,%(apt_ident)s,%(rwy_ident)s,%(nav_elev_ft)s, "
    sql += "%(nav_freq_khz)s,%(nav_freq_mhz)s,%(nav_bearing_true)s,%(nav_var_deg)s,"
    sql += "%(nav_name)s,%(nav_suffix)s,"
    #sql += "nav_center_lon84,nav_center_lat84,"
    sql += "%(nav_range_nm)s,%(nav_bias_nm)s,%(nav_standalone)s,%(nav_no_freq)s,%(nav_xplane_code)s,"
    sql += "ST_Transform(ST_GeomFromText(%(nav_center)s, 4326),3857)); "

    """
    sql += "?,?,?,?, "
    sql += "?,?,?,?,"
    sql += "?,?,"
    #sql += "nav_center_lon84,nav_center_lat84,"
    sql += "?,?,?,?,?,"
    sql += "ST_Transform(ST_GeomFromText(?, 4326),3857)); "
    """
    #sql_command = sql.format(**params)
    #sql += "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
    """
    sql = '''INSERT INTO navaid (nav_ident,apt_ident,rwy_ident,nav_elev_ft,nav_freq_khz,nav_freq_mhz,nav_bearing_true,nav_var_deg,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,nav_bias_nm,nav_standalone,nav_no_freq,nav_xplane_code,nav_center)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
    """
    """
    params = [nav_ident,apt_ident,rwy_ident,nav_elev_ft,nav_freq_khz,nav_freq_mhz,nav_bearing_true,nav_var_deg,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,nav_bias_nm,nav_standalone,nav_no_freq,nav_xplane_code,nav_center]
    """
    #print "Inserted: "+nav_ident

    #try:
    db.Cur.execute(sql, params)


#except:
#	print "Database Error, check sql and parameters."



##############################################################################################################
# XPlane Nav 810 Data specs
##############################################################################################################
#  2 NDB (Non-Directional Beacon)                       Includes NDB component of Locator Outer Markers (LOM)
#  3 VOR (including VOR-DME and VORTACs)                Includes VORs, VOR-DMEs and VORTACs
#  4 Localiser component of an ILS
#  5 Localiser component of a localiser-only approach   Includes for LDAs and SDFs
#  6 Glideslope component of an ILS                     Frequency shown is paired frequency, not the DME channel
#  7 Outer markers (OM) for an ILS                      Includes outer maker component of LOMs
#  8 Middle markers (MM) for an ILS
#  9 Inner markers (IM) for an ILS

# 12 DME, including the DME component of an ILS,        Frequency display suppressed on X-Plane's charts
#    VORTAC or VOR-DME                                          

# 13 Stand-alone DME, or the DME component              Frequency will displayed on X-Plane's charts
#    of an NDB-DME        
##############################################################################################################
def insert_marker(line):
    """Insert a marker

        The threshold table is queried to find the esiting threshod from apt_dat
        If found the then marker is inserted and one of mm_id, om_id, im_id updated
        Else the marker is inserted and "ident_lost" set to the unfound matching runway
    """

    #print "line=", line
    parts = ut.xsplit(line)
    #print parts

    apt_ident = parts[8]
    ident = parts[9]

    sql = "select threshold.thr_id from threshold "
    sql += "inner join airport on airport.apt_id = threshold.apt_id "
    sql += " where airport.apt_ident = %(apt_ident)s and threshold.ident =  %(ident)s "
    db.Cur.execute(sql, dict(apt_ident=apt_ident, ident=ident))
    rows = db.Cur.fetchall()
    #print "MM=", rows, len(rows)

    thr_id = None
    ident_lost = ""
    if len(rows) > 0:
        ## Found a matching threshold from apt_dat
        thr_id = rows[0][0]
    else:
        ## not row found so set ident_lost
        ident_lost = "%s-%s" % (apt_ident, ident)

    ## Set the marker ID (maybe same as row_code ?)
    mcode = parts[-1]
    if mcode == "IM":
        mt_id = 9
    elif mcode == "MM":
        mt_id = 8
    elif mcode == "OM":
        mt_id = 7

    if thr_id:
        ## Update the threshold and om_id, im_id or mm_id
        #col_id = "%s_id" % mcode.lower() # make mm_id from MM
        col_id = mcode.lower()  # make mm_id from MM
        point = ut.mk_point(lat=parts[1], lon=parts[2], alt=parts[3].strip())
        sql = "update threshold "
        #sql += " set " + col_id + " = %(marker_id)s "
        sql += " set " + col_id + " = ST_Transform(ST_GeomFromText(%(point)s, 4326),3857)  "
        sql += " where thr_id = %(thr_id)s"
        #db.Cur.execute(sql, dict(thr_pk=thr_id, marker_id=marker_id, point=point))
        db.Cur.execute(sql, dict(thr_id=thr_id, point=point))
        db.Con.commit()


def insert_ndb(line, src_name):
    """Inserts a `2` NDB Non-directional beacon
    """
    parts = ut.xsplit(line)
    point = ut.mk_point(lat=parts[1], lon=parts[2], alt=parts[3].strip())
    #elevation_ft = parts[3].strip()

    #print parts
    ## Insert navaid
    sqli = "insert into navaid("
    sqli += " ident, name, ntype_id, freq, range_nm, search, "
    sqli += " point, src_name, src_src "
    sqli += " )values ("
    sqli += " %(ident)s, %(name)s, %(navaid_type_id)s,  %(freq)s, %(range_nm)s, %(search)s,"
    sqli += " ST_Transform(ST_GeomFromText(%(point)s, 4326),3857), %(src_name)s, %(src_src)s  "
    sqli += ") returning navaid_id; "
    name = " ".join(parts[8:-1])
    ident = parts[7].strip()
    params = dict(ident=ident,
                  point=point,
                  navaid_type_id=2,  #elevation_ft=parts[3].strip(),
                  freq=parts[4].strip(),
                  range_nm=parts[5].strip(),
                  name=name, search=ident.upper() + name.upper(),
                  src_name=src_name,
                  src_src=line
    )
    #print params
    db.Cur.execute(sqli, params)
    db.Con.commit()
    navaid_pk = db.Cur.fetchone()[0]
    #print "NDB=", parts[7].strip(), navaid_pk
    return navaid_pk


def insert_vor(line, src_name):
    """Inserts a rowcode `3` VOR directional beacon


    .. code-block:: text

        3  43.88802800  000.87286100    896 11480 120   -2.0 AGN  AGEN-Gaudonville VOR-DME
        rc lat          lon
    """
    parts = ut.xsplit(line)
    point = ut.mk_point(lat=parts[1], lon=parts[2], alt=parts[3].strip())

    #print parts
    ## Insert navaid
    sqli = "insert into navaid("
    sqli += " ident, name, ntype_id, freq, range_nm, search, "
    sqli += " point, src_name, src_src "
    sqli += " )values ("
    sqli += " %(ident)s, %(name)s,  %(ntype_id)s, %(freq)s, %(range_nm)s, %(search)s,"
    sqli += " ST_Transform(ST_GeomFromText(%(point)s, 4326),3857), %(src_name)s, %(src_src)s  "
    sqli += ") returning navaid_id; "
    name = " ".join(parts[8:-1])
    ident = parts[7].strip()
    params = dict(ident=ident, point=point, ntype_id=3,
                  freq=parts[4].strip(),
                  range_nm=parts[5].strip(),
                  name=name,
                  search=ident.upper() + name.upper(),
                  src_name=src_name,
                  src_src=line
    )
    #print params
    db.Cur.execute(sqli, params)
    #db.Con.commit()
    marker_id = db.Cur.fetchone()[0]


def insert_dme(line, src_name):
    """Inserts a rowcode `3` VOR directional beacon


    .. code-block:: text

        3  43.88802800  000.87286100    896 11480 120   -2.0 AGN  AGEN-Gaudonville VOR-DME
        rc lat          lon
    """
    parts = ut.xsplit(line)
    point = ut.mk_point(lat=parts[1], lon=parts[2], alt=parts[3].strip())

    #print parts
    ## Insert navaid
    sqli = "insert into navaid("
    sqli += " ident, name, ntype_id, freq, range_nm, search, "
    sqli += " point, src_name, src_src "
    sqli += " )values ("
    sqli += " %(ident)s, %(name)s,  %(ntype_id)s, %(freq)s, %(range_nm)s, %(search)s,"
    sqli += " ST_Transform(ST_GeomFromText(%(point)s, 4326),3857), %(src_name)s, %(src_src)s  "
    sqli += ") returning navaid_id; "
    name = " ".join(parts[8:-1])
    ident = parts[7].strip()
    params = dict(ident=ident, point=point, ntype_id=12,
                  freq=parts[4].strip(),
                  range_nm=parts[5].strip(),
                  name=name,
                  search=ident.upper() + name.upper(),
                  src_name=src_name,
                  src_src=line
    )
    #print params
    db.Cur.execute(sqli, params)
    #db.Con.commit()
    marker_id = db.Cur.fetchone()[0]


def update_ils(line):
    """Inserts a rowcode `4` ILS


    .. code-block:: text

        0  1           2                 3  4      5      6       7    8    9   10
        4  42.37710200 -071.02169100     19 11070  18     315.261 ILIP KBOS 33L ILS-cat-I
        rc lat          lon            elev freq   range  heading idenr apt rwy type
    """
    print "update_ils", line
    parts = ut.xsplit(line)
    #print parts

    apt_ident = parts[8]
    ident = parts[9]

    sql = "select threshold.thr_id from threshold "
    sql += "inner join airport on airport.apt_id = threshold.apt_id "
    sql += " where airport.apt_ident = %(apt_ident)s and threshold.ident =  %(ident)s "
    db.Cur.execute(sql, dict(apt_ident=apt_ident, ident=ident))
    rows = db.Cur.fetchall()
    thr_id = None
    ident_lost = ""
    if len(rows) > 0:
        ## Found a matching threshold from apt_dats
        thr_id = rows[0][0]
    else:
        ## not row found so set ident_lost
        ident_lost = "%s-%s" % (apt_ident, ident)

    if thr_id:

        ## Update the threshold and om_id, im_id or mm_id
        #col_id = "%s_id" % mcode.lower() # make mm_id from MM
        point = ut.mk_point(lat=parts[1], lon=parts[2], alt=parts[3].strip())
        ## pete hack to calculate runwaycenter
        #rwy_middle = Geodesic.WGS84.Direct(float(t0.lat),float(t0.lon), float(t0.heading), float(rwy.length_m / 2))
        hdgg = float(parts[6]) + 180
        if hdgg > 360:
            hdgg = hdgg - 360

        dist = float(parts[5]) * NM_2_M
        extent_po = Geodesic.WGS84.Direct(float(parts[1]), float(parts[2]), hdgg, dist)
        # umm maybe we need to calc middle of displaced	??
        extent = ut.mk_point(lat=str(extent_po["lat2"]), lon=str(extent_po["lon2"]), alt=parts[3].strip())

        sql = "update threshold "
        #sql += " set " + col_id + " = %(marker_id)s "
        sql += " set ils_freq = %(freq)s, "
        sql += " loc_hdg = %(loc_hdg)s,  "
        sql += " loc_point = ST_Transform(ST_GeomFromText(%(point)s, 4326),3857),  "
        sql += " loc_extent = ST_Transform(ST_GeomFromText(%(extent)s, 4326),3857)  "
        sql += " where thr_id = %(thr_id)s "
        #db.Cur.execute(sql, dict(thr_pk=thr_id, marker_id=marker_id, point=point))
        db.Cur.execute(sql, dict(thr_id=thr_id, point=point,
                                 freq=parts[4].strip(), loc_hdg=parts[6].strip(),
                                 loc_range=parts[5].strip(), extent=extent
        ))
        db.Con.commit()
        print "yes", hdgg, dist
    else:
        print "no"


def update_gs(line):
    """Inserts a rowcode `6` ILS


    .. code-block:: text

        0  1           2                 3  4      5      6       7    8    9   10
        6  64.13363889 -021.94091667     48 10990  10  350175.260 IRK  BIRK 19  GS
        rc lat          lon            elev freq   range  heading idenr apt rwy type
    """
    print "update_gs", line
    parts = ut.xsplit(line)
    #print len(parts), parts
    if len(parts) < 10:
        print "OOOOOOOOOPS", line
        #YES
        return
    apt_ident = parts[8]
    ident = parts[9]

    sql = "select threshold.thr_id from threshold "
    sql += "inner join airport on airport.apt_id = threshold.apt_id "
    sql += " where airport.apt_ident = %(apt_ident)s and threshold.ident =  %(ident)s "
    db.Cur.execute(sql, dict(apt_ident=apt_ident, ident=ident))
    rows = db.Cur.fetchall()
    thr_id = None
    ident_lost = ""
    if len(rows) > 0:
        ## Found a matching threshold from apt_dats
        thr_id = rows[0][0]
    else:
        ## not row found so set ident_lost
        ident_lost = "%s-%s" % (apt_ident, ident)

    if thr_id:

        ## Update the threshold and om_id, im_id or mm_id
        #col_id = "%s_id" % mcode.lower() # make mm_id from MM
        point = ut.mk_point(lat=parts[1], lon=parts[2], alt=parts[3].strip())
        ## pete hack to calculate runwaycenter
        #rwy_middle = Geodesic.WGS84.Direct(float(t0.lat),float(t0.lon), float(t0.heading), float(rwy.length_m / 2))
        #hdgg = float(parts[6])
        #dist = float(parts[5]) * 100
        #//extent_po = Geodesic.WGS84.Direct(float(parts[1]),float(parts[2]), hdgg, dist)
        # umm maybe we need to calc middle of displaced	??
        extent = None  #sut.mk_point(lat=str(extent_po["lat2"]), lon=str(extent_po["lon2"]), alt=parts[3].strip())

        sql = "update threshold "
        #sql += " set " + col_id + " = %(marker_id)s "
        sql += " set "  #ils_freq = %(freq)s, "
        sql += " gs_deg = %(gs_deg)s,  "
        sql += " gs_point = ST_Transform(ST_GeomFromText(%(point)s, 4326),3857)  "
        #sql += " loc_extent = ST_Transform(ST_GeomFromText(%(extent)s, 4326),3857)  "
        sql += " where thr_id = %(thr_id)s "
        #db.Cur.execute(sql, dict(thr_pk=thr_id, marker_id=marker_id, point=point))
        db.Cur.execute(sql, dict(thr_id=thr_id, point=point,
                                 gs_deg=3

        ))
        db.Con.commit()
        print "yes", apt_ident, ident
    else:
        print "no", apt_ident, ident


def nuke_data():
    for t in ['navaid']:
        sql = "delete from %s;" % t
        db.Cur.execute(sql)
        db.Con.commit()


##############################################################################################
def import_nav_dat(ntype=None):
    """Imports the nav_dat"""



    marker_count = 1000
    c = 0

    xrec = conf.get_current()
    xdate = xrec['date']



    shard_dir = conf.work_dir("/raw_data/nav")


    if ntype != None:
        if ntype == "vor":
            file_path = "/home/fgxx/fgx-navdata/temp/nav.3.dat"

        if ntype == "markers":
            for marker_code in [RC.im, RC.mm, RC.om]:
                file_path = "%s/%s.%s.dat" % (shard_dir, marker_code, xdate)
                process_file(file_path, xrec)

        process_file(file_path, xrec)
        return

    nuke_data()
    for i in RC.list():
        nt = RC.ntype(i)

        file_path = "%s/%s.%s.dat" % (shard_dir, nt, xdate)
        print file_path
        process_file(file_path, xrec)

    ## vor
    #file_path = "/home/fgxx/fgx-navdata/temp/nav.3.dat"

    ## ils
    #file_path = "/home/fgxx/fgx-navdata/temp/nav.4.dat"

    ## gs
    #file_path = "/home/fgxx/fgx-navdata/temp/nav.6.dat"

    ## markers
    #file_path = "/home/fgxx/fgx-navdata/temp/nav.7.dat"
    #file_path = "/home/fgxx/fgx-navdata/temp/nav.8.dat"
    #file_path = "/home/fgxx/fgx-navdata/temp/nav.9.dat"

    # dme with Vortac + vor + ILS
    #file_path = "/home/fgxx/fgx-navdata/temp/nav.12.dat"
    # dme with NDB
    #file_path = "/home/fgxx/fgx-navdata/temp/nav.13.dat"

def process_file(file_path, xrec):

    src_name = "xplane-%s" % xrec['date']
    print "importing", file_path
    c = 0
    with open(file_path) as dat_file:

        for line in dat_file:
            c += 1
            row_code = int(line.split(" ")[0])

            #print c, row_code
            ## Approach Markers  - updates threshold
            # Marker Beacon, Outer (OM), Middle (MM) and Inner (IM) Markers
            if row_code in [RC.im, RC.mm, RC.om]:
                insert_marker(line)

            ## NDB station
            elif row_code == RC.ndb:
                insert_ndb(line, src_name)

            ## VOR Station
            elif row_code == RC.vor:
                insert_vor(line, src_name)

            ## DME Station
            elif row_code == RC.dme or row_code == RC.dme_ils:
                what = line.split(" ")[-1].strip()
                if what in ['VOR-DME', "NDB-DME", "DME", "VORTAC"]:
                    insert_dme(line, src_name)
                else:
                    if what in ['TACAN']:
                        pass  #print "skip=", what
                    else:
                        print "????=", what

            elif row_code in [RC.loc_ils1, RC.loc_ils2]:
                #print "localiser alive, check, check"
                update_ils(line)

            elif row_code == RC.gs:
                #print "localiser alive, check, check"
                update_gs(line)

            else:
                print "skip", c, line[0:10]

            """
            spaceremoved = " ".join(line.split())
            list = spaceremoved.split(" ")
            listlen = len(list)

            nav_standalone = "0"
            nav_no_freq = "1"

            #try:

            nav_xplane_code = str(list[0])
            nav_center_lat84 = str(list[1])
            nav_center_lon84 = str(list[2])
            nav_elev_ft = str(list[3])

            class Navaid:
                range = None
                ident = None
                name = None
            """

            # DME, Distance Measuring Equipment
            if line.startswith("xx12 ") or line.startswith("xx13 "):
                nav_freq_mhz = str(list[4])
                nav_range_nm = str(list[5])
                nav_bias_nm = str(list[6])
                nav_ident = str(list[7])
                #apt_ident = str(list[8])
                #rwy_ident = str(list[9])
                nav_name = str(list[10:listlen]).replace("', '", " ").replace("['", "").replace("']", "").replace("[]",
                                                                                                                  "")
                # specifier is not separated in xplane data, we need the last one
                nav_suffix = str(list[listlen - 1])
                # 12 = Suppress frequency = 1, 13 = display frequency = 0
                if line.startswith("12 "):
                    nav_no_freq = "1"
                else:
                    nav_no_freq = "0"

                # When DME-ILS there is apt identifier and runway number, but no name
                if nav_suffix == "DME-ILS":
                    apt_ident = str(list[8])
                    rwy_ident = str(list[9])
                    nav_name = None

                else:
                    apt_ident = None
                    nav_name = str(list[8:listlen - 1]).replace("', '", " ").replace("['", "").replace("']",
                                                                                                       "").replace("[]",
                                                                                                                   "")
                insert_navaid(nav_ident, apt_ident, rwy_ident, nav_elev_ft, None, nav_freq_mhz, None, None, nav_name,
                              nav_suffix, nav_center_lon84, nav_center_lat84, nav_range_nm, nav_bias_nm, None,
                              nav_no_freq, nav_xplane_code)

            #except:
            #pass
            ## We commit every 1000 to make faster
            if c % 200 == 0:
                print c
                db.Con.commit()
            c += 1

        db.Con.commit()


def postprocesscircles():
    # Doing geometry updates in navaid
    sqlnav = "SELECT * from navaid"
    db.Cur.execute(sqlnav)
    allnav = cur.fetchall()
    conn.commit()

    countcircle = 0

    for rownav in allnav:

        # query gives lon/lat (postgis x/y) as text for the center point in reprojected format
        sql2 = "UPDATE navaid SET nav_center_lon=ST_X(nav_center), nav_center_lat=ST_Y(nav_center) WHERE nav_pk=" + str(
            rownav[0]) + ";"
        cur.execute(sql2)

        conn.commit()

        latsql = "SELECT nav_center_lat84,nav_center_lon84,nav_range_nm FROM navaid WHERE nav_pk=" + str(
            rownav[0]) + ";"
        cur.execute(latsql)
        conn.commit()

        latlon = cur.fetchone()

        # Do not draw circles where you can't find a range, you
        if latlon[2] != None:
            lat84 = latlon[0]
            lon84 = latlon[1]
            navrange = int(latlon[2]) * 1852  # getting the range in meter

            # Drawing the range polygons

            circlerange = drawcircle(navrange, lon84, lat84)
            thiscircles = circlerange[:-2] + "))"

            rangesql = "UPDATE navaid SET nav_range_poly=ST_Transform(ST_GeometryFromText('" + thiscircles + "', 4326),3857) WHERE nav_pk=" + str(
                rownav[0]) + ";"
            cur.execute(rangesql)
            conn.commit()

            countcircle += 1
            print "Drawing circles for navaid range: " + str(rownav[1]) + " " + str(countcircle)





def shard(xrec):
    """
    Splits the navdata into files named nav.XX.dat where XX is the code
    """

    write_files = {}

    input_file = conf.work_dir("/xplane_unzipped/%s/earth_nav.dat" % xrec['zip_dir'])


    with open(input_file) as readnav:
        c = 0
        for line in readnav:


            if c < 3:
                pass  #print "skip", c, line

            else:

                row_code = line.split(" ")[0].strip()
                if row_code != "99":
                    if not row_code in write_files:
                        ntype = RC.ntype(row_code)
                        s_path = conf.work_dir("/raw_data/nav/%s.%s.dat" % (ntype, xrec['date']) )
                        #print s_path
                        write_files[row_code] = open(s_path, "w")

                    write_files[row_code].write(line)

            if c == 100:
                pass  #sys.exit(0)

            c += 1
            print c, line

    for row_code in write_files.keys():
        write_files[row_code].close()
