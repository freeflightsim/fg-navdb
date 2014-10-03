#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#
# Better remove the bad design with the globals instead. Thanks.

import sys, time, datetime, csv, os, re, psycopg2, yaml, warnings
import json

from navimport import conf
from navimport import db

def get_json(file_name):
	fp = conf.ROOT_PATH + "/conf/navdb_data/%s.json" % file_name 
	f = open(fp, 'r')
	data =  json.load(f)
	f.close()
	return data

def import_lookups():
	
	## Delete existing rows if any
	for t in ["approach_light", "beacon_type", "freq_type", "runway_surface", "marker_type", "nav_type"]:
		sql = "delete from %s;" % t;
		db.Cur.execute(sql)
	db.Con.commit()	
	print " > Deleted existing data"
	##========================================================
	

	## Beacons types
	data = get_json( "beacon_type" )
	sql = "insert into beacon_type(beacon_id, light, description)values(%(beacon_id)s, %(light)s, %(description)s)";
	for r in data['rows']:
		db.Cur.execute(sql, r)
	db.Con.commit()	   
	print " > beacon_type"


	## Frequence Type
	data = get_json( "freq_type" )
	sql = "insert into freq_type(type_id, freq, freq_description)values(%(type_id)s, %(freq)s, %(freq_description)s)";
	for r in data['rows']:
		db.Cur.execute(sql, r)
	db.Con.commit()
	print " > beacon_type"

	## Marker Type
	data = get_json( "marker_type" )
	sql = "insert into marker_type(marker_type_id, marker_code)values(%(marker_type_id)s, %(marker_code)s )";
	for r in data['rows']:
		db.Cur.execute(sql, r)
	db.Con.commit()
	print " > marker_type"
	
	## navaid Type

	data = get_json( "nav_type" )
	sql = "insert into nav_type(ntype_id, ntype, ntype_label)values(%(ntype_id)s, %(ntype)s, %(ntype_label)s )";
	for r in data['rows']:
		db.Cur.execute(sql, r)
	db.Con.commit()
	print " > nav_type"
	
	## Runway Surface
	data = get_json( "runway_surface" )
	sql = "insert into runway_surface(surface_id, surface)values(%(surface_id)s, %(surface)s)";
	for r in data['rows']:
		db.Cur.execute(sql, r)
	db.Con.commit()
	print " > runway_surface"
	
def insert_rows(sql, rows):
	for r in rows:
		db.Cur.execute(sql, r)
	db.Con.commit()
