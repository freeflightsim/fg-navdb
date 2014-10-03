FlightGear NavDb
===============================

- This project imports xplane data and delivers a json api
- Visit http://navdb.freeflightsim.org

The project has two core parts
- navimport/ - a bunch of python scripts to import the data
- navdb/ - a golang web server using the revel framework


Requirements:
-------------------
- A linux server with root/sudo access and gcc (dev platform is kubuntu/debian)
- Postgres 9 + Postgis2 database
- golang 1.3 - for development
- python 2.6+ - for importing


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






