# -*- coding: utf-8 -*-
# author: pete@daffodil.uk.com

import os
import sys
# import json
import configparser

from fabric.api import env, local, run, cd, sudo, prompt
from fabric import colors

# from webtest import TestApp

## Test app
#APP = None

"""
REVEL DOES NOT READ missing[default]

PROJECT_ROOT = os.path.abspath( os.path.dirname(__file__) )

## This fails
f = open( PROJECT_ROOT + "/conf/app.conf")
config_str = f.read()
f.close()

config = configparser.SafeConfigParser() # = json.loads(open(PROJECT_ROOT + "/config.json", "r").read())
config.read(config_str)

print config
"""

env.hosts = ['navdb.freeflightsim.org']
env.user = "fg"
env.password = "using-ssl-key"
env.use_ssh_config = True # this is using ~/.ssh/config = sshkey login
#env.shell = "/bin/sh -c"

#LIVE_ROOT = "/home/fg/fg-navdb"

import navimport.conf
import navimport.db

import navimport.xplane.lookups
import navimport.xplane.nav_dat
import navimport.xplane.apt_dat
import navimport.xplane.fix_dat

import navimport.procedures.xml_import


def hotfix():
	"""Pushed latest shit and hot patch to server"""
	print "In a Sweat.yet !"
	local("git commit -a -m")

	d_ploy()


def d_ploy():
	"""Deploys and restarts live server"""
	local("git push origin --all")
	with cd(LIVE_ROOT):
		run("git pull")


def upserver():
	with cd(LIVE_ROOT):
		run("git pull")


def local_views():
	"""Create and udpate database view locally"""
	pass


def _get_config():

	conf = navimport.conf.get_config(verbose=True)
	print "_get_config()=", conf
	return conf

def _prompt_xid(text):
	inp = prompt(colors.red(text))

	xid = None
	if inp == "":
		return None

	try:
		xid = int(inp)
	except:
		return None

	return navimport.conf.get_xplane_zip_info(xid)


def status():
	"""Print out status"""
	_loadconfig()
	navimport.conf.print_status()

#============================================
# Xplane stuff
#=============================================
def x_list():
	"""List available xplane zips"""
	_loadconfig()




def x_download():
	"""Download the latest xplane zip"""
	#_loadconfig()
	conf = _get_config()
	#print conf['xplane']
	download_url = conf['xplane']['download']
	local("wget -P %s %s" % (navimport.conf.work_dir("/xplane_zips"), download_url))


def x_unzip(xid=None):
	"""Shard and xplane zip"""
	_loadconfig()
	navimport.conf.print_zips()

	xrec = None
	if xid == None:
		xrec = _prompt_xid("No to unzip >")
	else:
		xrec = navimport.conf.get_xplane_zip_info(0)

	if xrec != None:
		print xrec

		s = "unzip "
		s += " -d " + navimport.conf.work_dir("/xplane_unzipped/%s" % xrec['zip_dir'])
		s += " "
		s += navimport.conf.work_dir("/xplane_zips/%s" % xrec['file_name'])
		local(s)





def x_shard(xtype="all"):
	"""Shard and xplane zip"""
	_loadconfig()
	#navimport.conf.print_zips()

	xrec = navimport.conf.get_xplane_zip_info(0)

	if xrec != None:
		print xrec

		if xtype == "all":
			navimport.xplane.apt_dat.shard(xrec)
			#navimport.xplane.fix_dat.shard(xrec)
			#navimport.xplane.nav_dat.shard(xrec)


def db_create(what=""):
	_loadconfig()

	navimport.db.create_procedure()
	return

	if what == "all":
		navimport.db.drop_all()
		navimport.db.create_all()
		navimport.xplane.lookups.import_lookups()


def db_views():
	_loadconfig()

	navimport.db.create_views()


def imp_fix():
	"""Import `earth_fix.dat`"""
	_loadconfig()
	navimport.xplane.fix_dat.import_fix_dat()


def imp_nav(ntype=None):
	"""Import `earth_nav.dat`"""
	_loadconfig()
	navimport.xplane.nav_dat.import_nav_dat(ntype)


def imp_apt(apt_ident=None):
	"""Import `apt.dat`"""
	_loadconfig()
	navimport.xplane.apt_dat.import_airports(apt_ident)


##==========================================
def imp_procs():
	"""Import procedures"""

	_loadconfig()
	xml_files_path = navimport.conf.work_dir("/Sid_Star_XML")

	"""
	for file in os.listdir(xml_files_path):
		if file.endswith(".xml"):
			xml_blob_path = xml_files_path + "/" + file
			print xml_blob_path
	"""
	navimport.procedures.xml_import.process_airport("EGLL")

	return
	xml_blob_path = xml_files_path + "/EGLL.xml"
	sids_, stars, approaches = navimport.procedures.xml_import.parse_xml_file(xml_blob_path)
	sids = sids_[1]
	for ki in sorted(sids.keys()):
		sid = sids[ki]
		print "s=", sid['name'], sid['runways']
		for wp in sid['waypoints']:
			print wp
	return


def runserver():
	"""Start the HTTP and GoLang server"""
	local("revel run github.com/FreeFlightSim/fg-navdb")
