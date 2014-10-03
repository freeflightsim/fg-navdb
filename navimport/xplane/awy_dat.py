
#
# (c) 2012, Yves Sablonier, Zurich
# (c) 2013-2014, Pete Morgan, EGFF
# GPLv2 or later

import sys
import re


from navimport import conf
from navimport import db
from navimport import utils as ut

MAX_LINES_GUESS = 70300


def insert_temp(**kwargs):
	"""Insert  into the `airway temp` table"""
	
	sql = "insert into airway_temp("
	sql += "s_ident, s_point, e_ident, e_point, awy, bottom, top, airways"
	sql += ") values("
	sql += "%(s_ident)s, ST_Transform(ST_GeomFromText(%(s_point)s, 4326),3857),"
	sql += "%(e_ident)s, ST_Transform(ST_GeomFromText(%(e_point)s, 4326),3857),"
	sql += "%(awy)s, %(bottom)s, %(top)s, %(airways)s"
	sql += ");"
	#print sql
	db.Cur.execute(sql, kwargs)
	#db.Con.commit()


def import_awy_dat(file_path):

	
	inputfile = file_path + "/earth_awy.dat"
	c = 0
	with open(inputfile) as readnav:
		
		for line in readnav:
			c += 1
			
			# Skip first three lines, hope Robin Peel will never change this behaviour ;-)
			if c < 4:
				pass
			else:
				parts = ut.xsplit(line)
				if parts[0] == "99":
					
					return
				## 0      1         2           3      4         5           6 7   8   9
				## 00UPP  20.566668 -154.125000 FITES  20.794556 -153.000633 1 210 460 R578
				
				dic = dict( s_ident = parts[0],
							s_point = ut.mk_point(lat=parts[1], lon=parts[2]),
							e_ident = parts[3],
							e_point = ut.mk_point(lat=parts[4], lon=parts[5]),
							awy=parts[6],
							bottom=parts[7], top=parts[8],
							airways=parts[9].split("-")
							)
				#print dic
			
				insert_temp( **dic )
				## We commit every x  to make faster
				if c % 5000 == 0:
					print " > fix at = %s of %s - %s" %( c, MAX_LINES_GUESS,  parts[0])
					db.Con.commit()
			
	## commit any outstanding after rows at end of loop		
	db.Con.commit()


def create():
	create_tables()

def create_tables():
	"""Creates tables for `awy` """
	sql = """
	create table airway_temp (
	  x_pk serial NOT NULL,
	  s_ident character varying(6),
	  s_point geometry(Point,3857),
	  e_ident character varying(6),
	  e_point geometry(Point,3857),
	  awy smallint,
	  bottom smallint,
	  top smallint,
	  airways varchar(10) ARRAY,
	  
	  CONSTRAINT airway_temp_pkey PRIMARY KEY (x_pk)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
	db.Cur.execute(sql)
	db.Con.commit()



	