FlightGear NavDb
===============================

- This project imports xplane data and delivers a json api
- Visit http://navdb.freeflightsim.org

The project has two core parts
- navimport/ - a bunch of python scripts to import the data
- navdb/ - a golang web server using the revel framework

Mission
------------------
This is a bleeding edge idea to serve a stable
and regular updated "feed" fo FlightGear pilots

- it takes the latest xplane data, which is a huge tarball.zip
- and imports using python and the navimport/* hacks
-- into a postgis database
-- the postgis db is setup with views and
-- extract spatial data from the geometry machine
-- and convert to values eg lat/lon on the fly
- The golang application replies to queries for this data in various formats
-- at http://navdb.freeflightsim.org/
-- and soon websocket, kml and xml feed
- Next Gen
-- move all shell import from python to golang/revel and remote execution
-- automatic update of data, ie same as before
-- flag changes, new or moved,dead = latest
-- move import routines to golang, maybe manage

From Revel:
- yaml config and multi config
- create json api autodocs
- use pongo templating for inhertitance,
- create jinja2 interface so I can share same templates ;-)))
- replace fab with app or alike

Requirements:
-------------------
- A linux server with root/sudo access and gcc
- Postgres 9 + Postgis2 database
- python 2.6+ - for importing
- golang 1.3 - for development
- revel app framwork -  github.com/revel/revel


Run:
-------------
    revel run github.com/FreeFlightSim/fg-navdb
    
or for "config" and "port"
    
    revel run github.com/FreeFlightSim/fg-navdb dev 7777

Then visit
http://localhost:777/controlpanel


Contact & Support:
----------------------
This project needs help, contact
- pete at FreeFlightSim dot org
- peteffs at irc.flightgear.org






