
#
# (c) 2012, Yves Sablonier, Zurich
# (c) 2013-2014, Pete Morgan, EGFF
# GPLv2 or later

import sys
import re

from navimport import conf
from navimport import db
from navimport import utils as ut

MAX_LINES_GUESS = 120000
"""Guesstimates line count
    .. note::
        The import routine batch commits on this variable  and detect block then walk block
"""


def insert_fix(**kwargs):
    """Insert a fix into the `fix` table"""
    kwargs['fix_center'] = ut.mk_point(lon=kwargs['lon'], lat=kwargs['lat'], alt=0)
    
    """
    sql = "insert into fix(ident, major, point) values("
    sql += "%(ident)s, %(major)s, "
    sql += "ST_Transform(ST_GeomFromText(%(fix_center)s, 4326),3857));"
    """
    sql = "insert into navaid(ident, name, search, ntype_id, point) values("
    sql += "%(ident)s, %(ident)s,  %(ident)s, 201, "
    sql += "ST_Transform(ST_GeomFromText(%(fix_center)s, 4326),3857));"
    #print sql
    db.Cur.execute(sql, kwargs)

def shard(xrec=None):
    """Reads earth_fix.dat and inserts to `fix` table

    TODO:
        fix the NPOLE bug
    """

    xrec = conf.get_current()

    print "FIX_DAT: shard()", xrec
    zip_ver = xrec['zip_dir']

    xindex = []

    regEx = re.compile("[A-Z]{5}")

    inputfile = conf.work_dir("/xplane_unzipped/%s/earth_fix.dat" % (xrec['zip_dir']))
    c = 0
    print inputfile


    with open(inputfile) as readnav:

        for line in readnav:
            c += 1

            # Skip first three lines, hope Robin Peel will never change this behaviour ;-)
            if c < 4:
                pass
            else:

                if not line.startswith("99"):

                    lst = line.strip().split()
                    fix_ident = str(lst[2])

                    fixblob = None

                    if fix_ident == "NPOLE":
                        pass

                    else:

                        ## Write shard
                        blob_path = conf.raw_fix_path( xrec, fix_ident)
                        #print file_path, xrec

                        f = open(blob_path + ".txt", "w")
                        f.write(line)
                        f.close()

                        ## make dic
                        maj = True if regEx.match(fix_ident) else False
                        data = dict(
                                ident=fix_ident, major=maj, src=line,
                                lat=str(lst[0]), lon=str(lst[1])
                            )
                        json_path = blob_path + ".json"
                        conf.write_json(json_path, data)



                        xindex.append(fix_ident)


                    if c % 5000 == 0:
                        print " > fix: %s - %s of %s" % (fix_ident, c, MAX_LINES_GUESS)
                        #sys.exit(0)
                        #db.Con.commit()

    ## commit any outstanding after rows at end of loop
    #db.Con.commit()

def import_fix_dat(xrec=None):
    """Reads earth_fix.dat and inserts to `fix` table
    
    TODO:
        fix the NPOLE bug
    """
    xrec = conf.get_current()


    regEx = re.compile("[A-Z]{5}")
    
    inputfile = conf.work_dir("/xplane_unzipped/%s/earth_fix.dat" % (xrec['zip_dir']))
    c = 0
    with open(inputfile) as readnav:
        
        for line in readnav:
            c += 1
            
            # Skip first three lines, hope Robin Peel will never change this behaviour ;-)
            if c < 4:
                pass
            else:
            
                if not line.startswith("99"):
                    
                    lst = line.strip().split()
                    fix_ident = str(lst[2])
                    
                    if fix_ident == "NPOLE":
                        pass
                    
                    else:
                        #//fix_center_lat84 = str(lst[0])
                        #fix_center_lon84 = str(lst[1])
                        maj = 1 if regEx.match(fix_ident) else 0
                        # insert to db
                        insert_fix( 
                            **dict(
                                ident=fix_ident, major=maj,
                                lat=str(lst[0]), lon=str(lst[1])
                            )
                            )
                        
                    ## We commit every x  to make faster
                    if c % 5000 == 0:
                        print " > fix: %s - %s of %s" % (fix_ident, c, MAX_LINES_GUESS)

            
    idx_file = conf.raw_fix_path()

def DEADempty_fix_table():
    """Deletes all rows in the fix table"""
    sqlnuke = "delete from fix"
    conf.Cur.execute(sqlnuke)
    conf.Con.commit()

## Create View
def DEADcreate_v_fix_view():
    """Creates the v_fix view"""
    sql_view = """create or replace view v_fix as
    SELECT 
    fix.fix_ident, 
    fix.fix_center,
    ST_Y(ST_Transform(fix.fix_center, 4326)) as fix_lat84,
    ST_X(ST_Transform(fix.fix_center, 4326)) as fix_lon84
    
    FROM 
    fix"""
    conf.Cur.execute(sql_view)
    conf.Con.commit()


if __name__ == "__main__":
    
    inputfile = sys.argv[1]
    
    import_fix_dat()


