# -*- coding: utf-8 -*-


import sys
import os
import json
import datetime
import psycopg2

import db

MYSQL_DATE_FORMAT = "%Y-%m-%d"

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
""" The Root is this git's root"""

if not ROOT_PATH in sys.path:
    sys.path.insert(0, ROOT_PATH)

TEMP_DIR = ROOT_PATH + "/temp"
"""Temp directory TODO make this an arg"""

CONFIG_FILE = ROOT_PATH + "/conf/config.json"
"""Path to config.json"""

CONFIG = None


def work_path_exists(pth):
    """Check workspace dir exists, and the path exists"""
    if CONFIG['workspace_dir'] == None:
        return False
    if CONFIG['workspace_dir'].strip() == "":
        return False
    return os.path.exists(CONFIG['workspace_dir'] + pth)


def work_dir(xtra=""):
    return CONFIG['workspace_dir'] + xtra

def xzip_path(xrec):
    return

def xunzip_path(xrec):
    return

def raw_path(xrec):
    return

def raw_fix_path(xrec, fix_ident=None):
    p = work_dir() + "/raw_data/fix"
    if fix_ident:
        #/fix/abc/IDENT.v
        fix_subdir = p + "/" + fix_ident[0:4]
        if not os.path.exists(fix_subdir):
            os.makedirs(fix_subdir)
        return fix_subdir + "/%s.%s" % (fix_ident, xrec['xid'])
    return p + "/index.%s" % xrec['xid']




def read_ws_json(pth):
    return read_json(CONFIG['workspace_dir'] + pth)


def read_json(file_path):
    f = open(file_path)
    data = json.loads(f.read())
    f.close()
    return data


def write_json(file_path, data):
    f = open(file_path, "w")
    f.write(json.dumps(data, indent=4, sort_keys=True))
    f.close()


def config_exists():
    return os.path.exists(CONFIG_FILE)


# # maybe we need this
def load_config(verbose=False):
    global CONFIG
    ok = False
    if not config_exists():
        print "FATAL: The config file does not exist: `%s`" % CONFIG_FILE
        sys.exit(0)

    CONFIG = read_json(CONFIG_FILE)

    ## Read the current
    CONFIG['CURR'] = None
    if work_path_exists("/current.json"):
        CONFIG['CURR'] = read_ws_json("/current.json")

    ## Init Database
    dbuser_config = CONFIG['db_live']
    db.init_connect(dbuser_config)

    setup_shards()

def setup_shards():
    dir_path = work_dir("/raw_data")
    if not os.path.exists(dir_path):
        os.makedirs("%s" % dir_path)

    for d in ["apt","nav","awy"]:
        sdir = dir_path + "/" + d
        if not os.path.exists(sdir):
            os.makedirs("%s" % (sdir))


def set_current(id):
    zips = get_xplane_sources_list()
    data = zips[id]
    file_path = work_dir("/current.json")
    return write_json(file_path, data)


def get_current():
    file_path = work_dir("/current.json")
    return read_ws_json("/current.json")


def read_xplane_sources_list():
    return read_json(ROOT_PATH + "/conf/navdb_data/xplane.sources.json")


def get_xplane_zip_info(xid):
    lst = get_xplane_sources_list()
    return lst[xid]



def get_xplane_sources_list():

    cur_id = None
    current = get_current()
    if current:
        if "xid" in current:
            cur_id = str(current['xid'])

    data = read_xplane_sources_list()
    lst = []

    for idx, x in enumerate(data['zips']):
        x['file_name'] = os.path.basename(x['url'])
        x['zip_dir'] = x['file_name'][0:-4]
        x['downloaded'] = work_path_exists("/xplane_zips/" + x['file_name'])
        x['extracted'] = work_path_exists("/xplane_unzipped/" + x['zip_dir'])
        x['sharded'] = work_path_exists("/raw_shards/" + x['zip_dir'])
        x['current'] = str(x['xid']) == cur_id
        lst.append(x)
    return lst


def print_status():
    wp_dir = CONFIG['workspace_dir']

    print ">> Status ===================================="
    print "Item\t\tStatus\tInfo"
    print "----------------------------"
    print "config.json\t%s\t%s" % ( "OK" if config_exists() else "FAIL", CONFIG_FILE)
    print "workspace\t%s\t%s" % ( "Yes" if work_path_exists("") else " No", CONFIG['workspace_dir'] )

    print "\n"
    navimport.conf.get_xplane_zip_info()
    print_zips()


def print_zips():
    zips = get_xplane_sources_list()

    print  "XID: Curr Down\tUnzip\tShard\tDated\t\tZip"
    print "-------------------------------------------------------------------------------------------------"

    for x in zips:
        no_str = "%s:" % x['xid']
        curr = "<Y>" if x['current'] else "   "
        downloaded = "Yes" if x['downloaded'] else " - "
        extracted = "Yes" if x['extracted'] else " - "
        sharded = "Yes" if x['sharded'] else " - "
        date_py = datetime.datetime.strptime(x['date'], MYSQL_DATE_FORMAT).date()
        date_str = datetime.date.strftime(date_py, "%d %b %Y")
        print "%s %s\t%s\t%s\t%s\t%s\t%s" % (no_str, curr, downloaded, extracted, sharded, date_str, x['file_name'])



