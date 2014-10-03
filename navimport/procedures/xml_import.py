
import os
import re

from bs4 import BeautifulSoup

from navimport import conf
from navimport import db
from navimport import utils as ut

def get_xml_index():
    lst = []
    xml_files_path = conf.work_dir("/Sid_Star_XML")

    for file in os.listdir(xml_files_path):
        if file.endswith(".xml"):
            xml_blob_path = xml_files_path + "/" + file
            dic = dict(file_path=xml_blob_path, file_name=file)
            blob = parse_xml_blob(xml_blob_path)
            print "blob=", blob

def parse_xml_file(xml_file):

       ## Load procedures
    #xml_file = conf.work_dir("/Sid_Star_XML/%s.xml" % ident)
    if os.path.exists(xml_file):
        soup = BeautifulSoup(open(xml_file, "r"), "xml")

        def get_nodes(node_name, waypoints_name):
            xml_nodes = soup.find_all(node_name)
            index = []
            dic = {}
            for node in xml_nodes:
                name =  node['Name']
                rwys =  node.get('Runways')
                index.append(name)
                waypoints = []
                for wp in node.find_all(waypoints_name):
                    rec = {}
                    for w in wp.children:
                        #print w.name
                        if w.name != None: # WTF?
                            rec[str(w.name).lower()] = w.string
                    waypoints.append(rec)
                dic[name] = dict(name=name, waypoints=waypoints)
                if rwys:
                    dic[name]['runways'] = rwys
            return sorted(index), dic

        sids =  get_nodes("Sid", "Sid_Waypoint")
        stars = get_nodes("Star", "Star_Waypoint")
        approaches = get_nodes("Approach", "App_Waypoint")
        return sids, stars, approaches

def nuke_procs(apt_ident):

    sql = 'delete from procedure_wp '  #where apt_ident=%(apt_ident)s;'
    db.Cur.execute(sql, dict(apt_ident=apt_ident))

    sql = 'delete from procedure ' #where apt_ident=%(apt_ident)s;'
    db.Cur.execute(sql, dict(apt_ident=apt_ident))


def process_airport(apt_ident):
    print "PROCESS", apt_ident

    nuke_procs(apt_ident)

    xml_path, ok = get_xml_path(apt_ident)
    if ok:
        sidst, starst, approachest = parse_xml_file(xml_path)


        stars_idx = starst[0]
        stars = starst[1]

        for p_name in stars_idx:
            star = stars[p_name]
            #runways = star['runways'].split(",")
            print p_name
            print sorted(star.keys())

            dic = dict(apt_ident = apt_ident, ident=p_name, description="", ntype_id=5001, thr_id=None)

            proc_id = db_write_proc(dic)
            db_write_waypoints(proc_id, star['waypoints'])
            """
            for r in runways:
                sql = "select thr_id from v_threshold where apt_ident=%(apt_ident)s and ident = %(thr_ident)s; "
                db.Cur.execute(sql, dict(apt_ident = apt_ident, thr_ident=r))
                row = db.Cur.fetchone()
                print "R", row
                thr_id = row[0]
                dic = dict(apt_ident = apt_ident, ident=p_name, description="", ntype_id=3000, thr_id=thr_id)

                proc_id = db_write_proc(dic)
                db_write_waypoints(proc_id, sid['waypoints'])
            """


        sids_idx = sidst[0]
        sids = sidst[1]

        for p_name in sids_idx:
            sid = sids[p_name]
            runways = sid['runways'].split(",")
            print p_name, runways
            print sorted(sid.keys())

            for r in runways:
                sql = "select thr_id from v_threshold where apt_ident=%(apt_ident)s and ident = %(thr_ident)s; "
                db.Cur.execute(sql, dict(apt_ident = apt_ident, thr_ident=r))
                row = db.Cur.fetchone()
                print "R", row
                thr_id = row[0]
                dic = dict(apt_ident = apt_ident, ident=p_name, description="", ntype_id=3001, thr_id=thr_id)

                proc_id = db_write_proc(dic)
                db_write_waypoints(proc_id, sid['waypoints'])


def db_write_proc(dic):
    sql = "insert into procedure("
    sql += "apt_ident, ntype_id, ident, description, thr_id "
    sql += ") values ("
    sql += "%(apt_ident)s, %(ntype_id)s, %(ident)s, %(description)s, %(thr_id)s "
    sql += ")  returning proc_id;"
    db.Cur.execute(sql, dic)
    db.Con.commit()
    proc_id = db.Cur.fetchone()[0]
    return proc_id



def db_write_waypoints(proc_id, waypoints):

    for idx, wp in enumerate(waypoints):
        print "INS_", wp

        sql = "insert into procedure_wp( "
        sql += " proc_id, wp_no, ident, alt_ft, alt_restriction, point "
        sql += ") values ("
        sql += " %(proc_id)s, %(wp_no)s, %(ident)s, %(alt_ft)s, %(alt_restriction)s, "
        sql += "ST_Transform(ST_GeomFromText(%(point)s, 4326),3857)"
        sql += ");"
        pnt =ut.mk_point(lon=wp['longitude'], lat=wp['latitude'], alt=wp['altitude'])
        wdic = dict(proc_id=proc_id, ident=wp['name'], wp_no=idx,
                    alt_restriction=wp['altituderestriction'], alt_ft=wp['altitude'], point=pnt)
        db.Cur.execute(sql, wdic)
        db.Con.commit()

def get_xml_path(apt_ident):
    xml_blob_path = conf.work_dir("/Sid_Star_XML/%s.xml" % apt_ident)
    return xml_blob_path, os.path.exists(xml_blob_path)

def get_xml_list():
    lst = []
    xml_files_path = conf.work_dir("/Sid_Star_XML")

    for file in os.listdir(xml_files_path):
        if file.endswith(".xml"):
            xml_blob_path = xml_files_path + "/" + file
            parse_file(xml_blob_path)


