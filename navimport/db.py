import conf
import os
import psycopg2
import psycopg2.extras

Con = None
"""Connection to database"""

Cur = None
"""Database Cursor"""

views = ["v_airport", "v_runway", "v_threshold", "v_navaid", "v_fix",
         "v_procedure", "v_procedure_wp",
         "mv_airport", "mv_apt_10", "mv_apt_30",

         "mv_navaid", "mv_vor", "mv_runway_line", "mv_ils_line", "mv_threshold",
         "mv_im", "mv_om", "mv_mm",
         "mv_wp"
         ]

tables = ["approach_light", "beacon_type", "freq_type", "runway_surface",
          "airport", "runway", "threshold", "frequency", "sign",
          "fix", "navaid", "marker", "marker_type", "nav_type",
          "procedure", "procedure_wp",

]


def init_connect(db_dict):
    """Initialise the database connection with credentials"""

    # print dbu
    connectstring = "host=%s  user=%s password=%s dbname=%s" % (db_dict['server'],
                                                                db_dict['user'], db_dict['password'],
                                                                db_dict['database'])
    # print connectstring
    ## Create the connection (?is there an error here ?)
    global Con
    Con = psycopg2.connect(connectstring)

    global Cur
    ## Create the Cursoe (?is there an error here asks pete)
    Cur = Con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    ## idea is to return false and error maybe ??
    return True


# #====================================================

def create_all():
    """Creates (after dropping) all the db tables"""
    create_lookups()

    create_airport()
    create_runway()
    create_threshold()

    create_frequency()

    create_navaid()
    create_marker()
    create_sign()

    create_fix()

    create_procedure()

    create_views()

    create_functions()


# #===========================================================
def drop_all():
    """Drops all views and tables, views first then tables because of dependancy."""
    for v in views:
        drop_view(v)

    for t in tables:
        drop_table(t)


def drop_views():
    """Drops all views"""
    for v in views:
        drop_view(v)


def drop_view(view):
    """Drop database view"""
    sql = "drop view if exists %s;" % view
    print "drop view: `%s`" % view
    Cur.execute(sql)
    Con.commit()


def drop_table(table):
    """Drop database table"""
    sql = "drop table if exists %s;" % table
    print "drop table: `%s`" % table
    Cur.execute(sql)
    Con.commit()


##========================================================
def create_procedure():
    """Creates the **airport** table, imported at :py:func:`xplane.apt_dat.insert_apt` """
    print "create table: `%s`" % "procedure"
    drop_views()

    drop_table("procedure")
    drop_table("procedure_wp")

    sql = """
	CREATE TABLE procedure
	(
		proc_id serial NOT NULL,
		apt_ident character(4),
		ntype_id int,
		ident character varying(50),
		description character varying(255),
		thr_id int,
		CONSTRAINT proc_id PRIMARY KEY (proc_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqli = []
    sqli.append("CREATE INDEX procedure_apt_ident_idx ON procedure (apt_ident);")
    sqli.append("CREATE INDEX procedure_ntype_id_idx ON procedure (ntype_id);")
    sqli.append("CREATE INDEX procedure_thr_id_idx ON procedure (thr_id);")
    for si in sqli:
        Cur.execute(si)

    print "create table: `%s`" % "procedure_wp"
    sql = """
	CREATE TABLE procedure_wp
	(
		wp_id serial NOT NULL,
		proc_id int,
		wp_no int,
		ident character varying(50),
		procedure int,
		alt_ft int,
		alt_restriction character varying(50),
		hdg_crs int,
		hdg int,
		point geometry(Pointz,3857),
	  CONSTRAINT wp_id_idx PRIMARY KEY (wp_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqli = []

    sqli.append("CREATE INDEX procedure_wp_proc_id_idx ON procedure_wp (proc_id);")
    sqli.append("CREATE INDEX procedure_wp_no_idx ON procedure_wp (wp_no);")
    sqli.append("CREATE INDEX procedure_wp_ident_idx ON procedure_wp (ident);")

    for si in sqli:
        Cur.execute(si)

    Con.commit()

    create_views()

##========================================================
def create_airport():
    """Creates the **airport** table, imported at :py:func:`xplane.apt_dat.insert_apt` """
    print "create table: `%s`" % "airport"
    sql = """
	CREATE TABLE airport
	(
	  icao character(4),
	  apt_name character varying(255),
	  closed smallint,
	  apt_country character varying(8),
	  apt_type character varying(255),
	  beacon_id smallint,
	  elevation_m smallint,
	  authority smallint,
	  services character varying(1),
	  ifr character varying(1),
	  apt_size character varying(32),
	  center geometry(Point,3857),
	  apt_range_30nm geometry(Polygon,3857),
	  apt_range_10nm geometry(Polygon,3857),
	  apt_search character varying(255),
	  src_name character varying(50),
	  src_src character varying(255),
	  CONSTRAINT airport_icao PRIMARY KEY (icao)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqli = []
    #sqli.append("CREATE INDEX apt_ident_idx ON airport (apt_ident);")
    sqli.append("CREATE INDEX airport_name_idx ON airport (apt_name);")
    sqli.append("CREATE INDEX apt_search_idx ON airport (apt_search);")
    for si in sqli:
        Cur.execute(si)

    Con.commit()


def create_runway():
    """Creates the **runway** table, imported at :py:func:`xplane.apt_dat.insert_rwy` """
    print "create table: `%s`" % "runway"
    sql = """
	CREATE TABLE runway
	(
	  rwy_id serial NOT NULL,
	  icao character(4),
	  thr0_id integer,
	  thr1_id integer,
	  width_m character varying(32),
	  center geometry(Point,3857),
	  length_m smallint,
	  surface_id smallint,
	  shoulder_id smallint,
	  smoothness decimal(10,2),
	  center_lights smallint,
	  edge_lights smallint,
	  auto_dist_signs smallint,
	  rwy_poly geometry(Polygon,3857),
	  src_name character varying(50),
	  src_src character varying(255),
	  CONSTRAINT runway_idey PRIMARY KEY (rwy_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqli = []
    sqli.append("CREATE INDEX runway_icao_idx ON runway (icao);")
    sqli.append("CREATE INDEX runway_thr0_id_idx ON runway (thr0_id);")
    sqli.append("CREATE INDEX runway_thr1_id_idx ON runway (thr1_id);")
    sqli.append("CREATE INDEX runway_surface_id_idx ON runway (surface_id);")
    sqli.append("CREATE INDEX runway_shoulder_id_idx ON runway (shoulder_id);")
    for si in sqli:
        Cur.execute(si)

    Con.commit()


def create_threshold():
    """Creates the **threshold** table, imported at :py:func:`xplane.apt_dat.insert_threshold` """
    print "create table: `%s`" % "threshold"
    sql = """
	CREATE TABLE threshold
	(
	thr_id serial NOT NULL,
	recip_id integer,
	apt_id integer NOT NULL,
	ident character varying(32),
	reciprocal character varying(32),
	start geometry(Point,3857),
	displacement_m decimal(10,2),
	threshold geometry(Point,3857),
	hdg decimal(10,2),
	overrun character varying(32),
	marking character varying(8),
	app_light_id smallint,
	tdz_lights character varying(8),
	reil character varying(8),
	om geometry(Pointz,3857),
	mm geometry(Pointz,3857),
	im geometry(Pointz,3857),
	ils_freq decimal(10,2),
	loc_point geometry(Pointz,3857),
	loc_hdg  decimal(10,3),
	loc_range_nm smallint,
	loc_extent geometry(Pointz,3857),
	gs_point geometry(Pointz,3857),
	gs_deg  decimal(10,3),
    src_name character varying(50),
	src_src character varying(255),
	CONSTRAINT thr_idey PRIMARY KEY (thr_id)
	)
	WITH (
	OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqll = []
    sqll.append("CREATE INDEX threshold_thr_ident_idx ON threshold (ident);")
    #sqll.append("CREATE INDEX threshold_om_idx ON threshold (om_id);")
    #sqll.append("CREATE INDEX threshold_mm_idx ON threshold (mm_id);")
    #sqll.append("CREATE INDEX threshold_im_idx ON threshold (im_id);")
    for sql in sqll:
        Cur.execute(sql)

    Con.commit()


##==========================================
def create_frequency():
    """Creates the **frequency** table, imported at :py:func:`xplane.apt_dat.insert_freq` """
    print "create table: `%s`" % "frequency"
    sql = """
	CREATE TABLE frequency
	(
	  freq_id serial NOT NULL,
	  apt_id integer,
	  type_id smallint,
	  freq_mhz decimal(10, 3),
	  description character varying(255),
	  range_km smallint,
	  range_nm smallint,
	  center geometry(Point,3857),
	  CONSTRAINT frequency_idey PRIMARY KEY (freq_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sql = "CREATE INDEX freq_apt_id_idx ON frequency (apt_id);"
    Cur.execute(sql)

    sql = "CREATE INDEX freq_type_id_idx ON frequency (type_id);"
    Cur.execute(sql)

    Con.commit()


def create_navaid():
    """Creates the **navaid** table, imported at :py:func:`xplane.nav_dat` """
    print "create table: `%s`" % "navaid"
    sql = """
	CREATE TABLE navaid
	(
	  navaid_id serial NOT NULL,
	  ident character varying(6),
	  name character varying(100),
	  ntype_id smallint,
	  freq smallint,
	  range_nm smallint,
	  search character varying (100),
	  point geometry(Pointz,3857),
	  src_name character varying(50),
	  src_src character varying(255),
	  CONSTRAINT navaid_id_pk PRIMARY KEY (navaid_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqli = []
    sqli.append("CREATE INDEX navaid_ntype_id_idx ON navaid (ntype_id);")
    sqli.append("CREATE INDEX navaid_ident_idx ON navaid (ident);")
    sqli.append("CREATE INDEX navaid_name_idx ON navaid (name);")
    sqli.append("CREATE INDEX navaid_search ON navaid (search);")
    for si in sqli:
        Cur.execute(si)

    Con.commit()


def create_sign():
    print "create table: `%s`" % "sign"
    sql = """
	CREATE TABLE sign
	(
	  sign_id serial NOT NULL,
	  apt_id integer,
	  size_id integer,
	  orientation decimal(10,2),
	  point geometry(Point,3857),
	  text text,
	  src_name character varying(50),
	  src_src character varying(255),
	  CONSTRAINT sign_idey PRIMARY KEY (sign_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqli = []
    sqli.append("CREATE INDEX apt_id_idx ON sign (apt_id);")
    for si in sqli:
        Cur.execute(si)

    Con.commit()


def DEADcreate_ils():
    """Creates the **navaid** table, imported at :py:func:`xplane.nav_dat` """
    print "create table: `%s`" % "ils"
    sql = """
	CREATE TABLE ils
	(
	ils_id serial NOT NULL,
	thr_id integer,
	type_id smallint,
	freq_mhz numeric(10,3),
	description character varying(255),
	range_km smallint,
	range_nm smallint,
	center geometry(Point,3857),
	CONSTRAINT ils_id_idey PRIMARY KEY (ils_id)
	)
	WITH (
	OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqli = []
    #sqli.append("CREATE INDEX navaid_ident_idx ON navaid (ident);")
    #sqli.append("CREATE INDEX navaid_navaid_type_id_idx ON navaid (navaid_type_id);")
    #sqli.append("CREATE INDEX navaid_name_idx ON navaid (name);")
    for si in sqli:
        Cur.execute(si)

    Con.commit()


def create_marker():
    print "create table: `%s`" % "marker"
    sql = """
	CREATE TABLE marker
	(
	  marker_id serial NOT NULL,
	  thr_id integer,
	  marker_type_id integer NOT NULL,
	  elevation_ft smallint,
	  center geometry(Point,3857),
	  ident_lost character varying(32),
	  CONSTRAINT marker_idey PRIMARY KEY (marker_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sqli = []
    sqli.append("CREATE INDEX thr_id_idx ON marker (thr_id);")
    for si in sqli:
        Cur.execute(si)

    Con.commit()


##==========================================================================
def create_fix():
    print "create table: `%s`" % "fix"
    sql = """
	CREATE TABLE fix
	(
	  fix_id serial NOT NULL,
	  ident character varying(32),
	  major smallint,
	  point geometry(Point,3857),
	  CONSTRAINT fix_idey PRIMARY KEY (fix_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    sql = "CREATE INDEX fix_ident ON fix (ident);"
    Cur.execute(sql)

    #sql = "CREATE INDEX fix_ident_upper ON fix (upper(ident));"
    #Cur.execute(sql)

    Con.commit()


def create_airway_temp():
    print "create table: `%s`" % "airway_temp"
    sql = """
		create table airway_temp (
		x_id serial NOT NULL,
		s_ident character varying(6),
		s_point geometry(Point,3857),
		e_ident character varying(6),
		e_point geometry(Point,3857),
		awy smallint,
		bottom smallint,
		top smallint,
		airways varchar(10) ARRAY,
		
		CONSTRAINT airway_temp_idey PRIMARY KEY (x_id)
		)
		WITH (
		OIDS=FALSE
		);
	"""
    Cur.execute(sql)

    sqli = []
    sqli.append("CREATE INDEX thr_id_idx ON marker (thr_id);")
    for si in sqli:
        Cur.execute(si)

    Con.commit()


##==========================================================================			
def create_lookups():
    """Creates the lookup tables"""
    print "create table: `%s`" % "approach_light"
    ## Approach lights
    sql = """
	CREATE TABLE approach_light
	(
	  light_id serial NOT NULL,
	  light character varying(40),
	  description character varying(200),
	  CONSTRAINT app_light_id_idey PRIMARY KEY (light_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    ## Beacon type
    print "create table: `%s`" % "beacon_type"
    sql = """
	CREATE TABLE beacon_type
	(
	  beacon_id serial NOT NULL,
	  light character varying(40),
	  description character varying(200),
	  CONSTRAINT beacon_id_idey PRIMARY KEY (beacon_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    ## Freq type
    print "create table: `%s`" % "freq_type"
    sql = """
	CREATE TABLE freq_type
	(
	  type_id serial NOT NULL,
	  freq character varying(20),
	  freq_description character varying(50), 
	 CONSTRAINT freq_type_idey PRIMARY KEY (type_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    ## marker type
    print "create table: `%s`" % "marker_type"
    sql = """
	CREATE TABLE marker_type
	(
	  marker_type_id serial NOT NULL,
	  marker_code character varying(2),
	 CONSTRAINT marker_type_idey PRIMARY KEY (marker_type_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    ## Navaid type
    print "create table: `%s`" % "nav_type"
    sql = """
	CREATE TABLE nav_type
	(
	  ntype_id serial NOT NULL,
	  ntype character varying(10),
	  ntype_label character varying(50),
	  CONSTRAINT ntype_id_idey PRIMARY KEY (ntype_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)

    ## runway_surface
    print "create table: `runway_surface`"
    sql = """
	CREATE TABLE runway_surface
	(
	  surface_id serial NOT NULL,
	  surface character varying(20),
	  CONSTRAINT runway_surface_id_idey PRIMARY KEY (surface_id)
	)
	WITH (
	  OIDS=FALSE
	);
	"""
    Cur.execute(sql)
    Con.commit()


def create_functions():
    sql = """
	CREATE OR REPLACE FUNCTION generate_create_table_statement(p_table_name varchar)
	RETURNS text AS
	$BODY$
	DECLARE
		v_table_ddl   text;
		column_record record;
	BEGIN
		FOR column_record IN 
			SELECT 
				b.nspname as schema_name,
				b.relname as table_name,
				a.attname as column_name,
				pg_catalog.format_type(a.atttypid, a.atttypmod) as column_type,
				CASE WHEN 
					(SELECT substring(pg_catalog.pg_get_expr(d.adbin, d.adrelid) for 128)
					FROM pg_catalog.pg_attrdef d
					WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND a.atthasdef) IS NOT NULL THEN
					'DEFAULT '|| (SELECT substring(pg_catalog.pg_get_expr(d.adbin, d.adrelid) for 128)
								FROM pg_catalog.pg_attrdef d
								WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND a.atthasdef)
				ELSE
					''
				END as column_default_value,
				CASE WHEN a.attnotnull = true THEN 
					'NOT NULL'
				ELSE
					'NULL'
				END as column_not_null,
				a.attnum as attnum,
				e.max_attnum as max_attnum
			FROM 
				pg_catalog.pg_attribute a
				INNER JOIN 
				(SELECT c.oid,
					n.nspname,
					c.relname
				FROM pg_catalog.pg_class c
					LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
				WHERE c.relname ~ ('^('||p_table_name||')$')
					AND pg_catalog.pg_table_is_visible(c.oid)
				ORDER BY 2, 3) b
				ON a.attrelid = b.oid
				INNER JOIN 
				(SELECT 
					a.attrelid,
					max(a.attnum) as max_attnum
				FROM pg_catalog.pg_attribute a
				WHERE a.attnum > 0 
					AND NOT a.attisdropped
				GROUP BY a.attrelid) e
				ON a.attrelid=e.attrelid
			WHERE a.attnum > 0 
			AND NOT a.attisdropped
			ORDER BY a.attnum
		LOOP
			IF column_record.attnum = 1 THEN
				v_table_ddl:='CREATE TABLE '||column_record.schema_name||'.'||column_record.table_name||' (';
			ELSE
				v_table_ddl:=v_table_ddl||',';
			END IF;

			IF column_record.attnum <= column_record.max_attnum THEN
				v_table_ddl:=v_table_ddl||chr(10)||
						'    '||column_record.column_name||' '||column_record.column_type||' '||column_record.column_default_value||' '||column_record.column_not_null;
			END IF;
		END LOOP;

		v_table_ddl:=v_table_ddl||');';
		RETURN v_table_ddl;
	END;
	$BODY$
	LANGUAGE 'plpgsql' COST 100.0 SECURITY INVOKER;
	"""
    Cur.execute(sql)
    Con.commit()
    print "create function: `generate_create_table_statement`"


#########################################################################################################################
## VIEWS 
#########################################################################################################################
def create_views():
    """Creates the views"""

    drop_views()
    ## v_airport
    print "create view: `v_airport`"
    sql = """
	CREATE OR REPLACE VIEW v_airport AS 
	SELECT airport.apt_id, airport.apt_ident, airport.apt_name, airport.apt_search, airport.apt_size,
	beacon_type.light,
	airport.center, st_y(st_transform(airport.center, 4326)) AS center_lat, st_x(st_transform(airport.center, 4326)) center_lon,
	airport.elevation_m as elev_m, round(airport.elevation_m * 3.2808399,  0) as elev_ft
	FROM airport
	inner join beacon_type on beacon_type.beacon_id = airport.beacon_id;
	"""
    Cur.execute(sql)
    Con.commit()

    ## v_runway
    print "create view: `v_runway`"
    sql = """
	create or replace view v_runway as
	select 
	runway.rwy_id, runway.apt_id,
	airport.apt_ident,
	thr0_id, thr1_id,
	thr0.ident as thr0_ident, thr1.ident as thr1_ident,
	(thr0.ident || '-' || thr1.ident) as rwy,
	length_m, width_m, surface, to_char(thr0.displacement_m, 'FM990D00') as displacement0_m, to_char(thr1.displacement_m, 'FM990D00') as displacement1_m,
	runway.center as center, st_y(st_transform(runway.center, 4326)) AS center_lat, st_x(st_transform(runway.center, 4326)) center_lon,
	
	thr0.threshold as threshold0, st_y(st_transform(thr0.threshold, 4326)) AS thr0_lat, st_x(st_transform(thr0.threshold, 4326)) thr0_lon,
	thr0.start as start0, st_y(st_transform(thr0.start, 4326)) AS start0_lat, st_x(st_transform(thr0.start, 4326)) start0_lon,
	thr0.im as im0, st_y(st_transform(thr0.im, 4326)) AS im0_lat, st_x(st_transform(thr0.im, 4326)) im0_lon,
	thr0.mm as mm0, st_y(st_transform(thr0.mm, 4326)) AS mm0_lat, st_x(st_transform(thr0.mm, 4326)) mm0_lon,
	thr0.om as om0, st_y(st_transform(thr0.om, 4326)) AS om0_lat, st_x(st_transform(thr0.om, 4326)) om0_lon,
	
	thr0.loc_point as loc_point0, st_y(st_transform(thr0.loc_point, 4326)) AS loc_point0_lat, st_x(st_transform(thr0.loc_point, 4326)) loc_point0_lon,
	thr0.loc_extent as loc_extent0, st_y(st_transform(thr0.loc_extent, 4326)) AS loc_extent0_lat, st_x(st_transform(thr0.loc_extent, 4326)) loc_extent0_lon,
	thr0.gs_point as gs_point0, st_y(st_transform(thr0.gs_point, 4326)) AS gs_point0_lat, st_x(st_transform(thr0.gs_point, 4326)) gs_point0_lon,
	
	thr1.threshold as threshold1, st_y(st_transform(thr1.threshold, 4326)) AS thr1_lat, st_x(st_transform(thr1.threshold, 4326)) thr1_lon,
	thr1.start as start1, st_y(st_transform(thr1.start, 4326)) AS start1_lat, st_x(st_transform(thr1.start, 4326)) start1_lon,
	thr1.im as im1, st_y(st_transform(thr1.im, 4326)) AS im1_lat, st_x(st_transform(thr1.im, 4326)) im1_lon,
	thr1.mm as mm1, st_y(st_transform(thr1.mm, 4326)) AS mm1_lat, st_x(st_transform(thr1.mm, 4326)) mm1_lon,
	thr1.om as om1, st_y(st_transform(thr1.om, 4326)) AS om1_lat, st_x(st_transform(thr1.om, 4326)) om1_lon,

	thr1.loc_point as loc_point1, st_y(st_transform(thr1.loc_point, 4326)) AS loc_point1_lat, st_x(st_transform(thr1.loc_point, 4326)) loc_point1_lon,
	thr1.loc_extent as loc_extent1, st_y(st_transform(thr1.loc_extent, 4326)) AS loc_extent1_lat, st_x(st_transform(thr1.loc_extent, 4326)) loc_extent1_lon,
	thr1.gs_point as gs_point1, st_y(st_transform(thr1.gs_point, 4326)) AS gs_point1_lat, st_x(st_transform(thr1.gs_point, 4326)) gs_point1_lon
	
	from runway
	inner join airport on airport.apt_id = runway.apt_id
	inner join threshold thr0 on thr0.thr_id = runway.thr0_id
	inner join threshold thr1 on thr1.thr_id = runway.thr1_id 
	inner join runway_surface on runway_surface.surface_id = runway.surface_id;
	"""
    Cur.execute(sql)
    Con.commit()

    ## v_threshold
    print "create view: `v_threshold`"
    sql = """
	drop view if exists v_threshold;
	CREATE OR REPLACE VIEW v_threshold AS 
	SELECT threshold.thr_id, threshold.ident, threshold.reciprocal, threshold.apt_id, airport.apt_ident, threshold.hdg,
	threshold.start, st_y(st_transform(threshold.start, 4326)) AS start_lat, st_x(st_transform(threshold.start, 4326)) AS start_lon,
	threshold.threshold, st_y(st_transform(threshold.threshold, 4326)) AS threshold_lat, st_x(st_transform(threshold.threshold, 4326)) AS threshold_lon,
	to_char(threshold.displacement_m , 'FM990D00') as displacement_m,
	threshold.im, st_y(st_transform(threshold.im, 4326)) AS im_lat, st_x(st_transform(threshold.im, 4326)) im_lon,
	threshold.mm, st_y(st_transform(threshold.mm, 4326)) AS mm_lat, st_x(st_transform(threshold.mm, 4326)) mm_lon,
	threshold.om, st_y(st_transform(threshold.om, 4326)) AS om_lat, st_x(st_transform(threshold.om, 4326)) om_lon,
	threshold.loc_point, st_y(st_transform(threshold.loc_point, 4326)) AS loc_point_lat, st_x(st_transform(threshold.loc_point, 4326)) loc_point_lon,
	threshold.loc_extent, st_y(st_transform(threshold.loc_extent, 4326)) AS loc_extent_lat, st_x(st_transform(threshold.loc_extent, 4326)) loc_extent_lon
	
	FROM threshold
	JOIN airport ON airport.apt_id = threshold.apt_id;
	"""
    Cur.execute(sql)
    Con.commit()

    ## v_navaid
    print "create view: `v_navaid`"
    sql = """
	CREATE OR REPLACE VIEW v_navaid AS 
	SELECT navaid.navaid_id, navaid.ident, navaid.name, navaid.ntype_id, nav_type.ntype, navaid.search,
	navaid.point, st_y(st_transform(navaid.point, 4326)) AS lat, st_x(st_transform(navaid.point, 4326)) as lon,
	ST_Z(navaid.point) as elev_ft, ST_Z(navaid.point) * 0.3048 as elev_m
	FROM navaid
	JOIN nav_type ON nav_type.ntype_id = navaid.ntype_id;
	"""
    Cur.execute(sql)
    Con.commit()




    ## v_fix
    ## TODO rename shite
    print "create view: `v_fix`"
    sql = """
	create or replace view v_fix as
	SELECT 
	fix.fix_id, fix.ident, fix.major,
	fix.point,
	ST_Y(ST_Transform(fix.point, 4326)) as lat,
	ST_X(ST_Transform(fix.point, 4326)) as lon
	FROM 
	fix;
	"""
    Cur.execute(sql)
    Con.commit()

    print "create view: `v_procedure`"
    sql = """
	CREATE OR REPLACE VIEW v_procedure AS
	SELECT procedure.proc_id,  procedure.ident,
	airport.apt_ident, airport.apt_name,
	nav_type.ntype
	FROM procedure
	inner join nav_type on nav_type.ntype_id = procedure.ntype_id
    inner join airport on airport.apt_ident = procedure.apt_ident
	"""
    Cur.execute(sql)
    Con.commit()

    print "create view: `v_procedure_wp`"
    sql = """
	CREATE OR REPLACE VIEW v_procedure_wp AS
	SELECT wp_id,  proc_id, wp_no,  ident, alt_ft, alt_restriction,
	ST_Y(ST_Transform(point, 4326)) as lat,
	ST_X(ST_Transform(point, 4326)) as lon
	FROM procedure_wp
	"""
    Cur.execute(sql)
    Con.commit()

    ##----MAPS
    ## m_navaid
    print "create view: `mv_navaid`"
    sql = """
	CREATE OR REPLACE VIEW mv_navaid AS
	SELECT navaid.ident, navaid.name, navaid.ntype_id, nav_type.ntype,
	navaid.point,
	ST_Z(navaid.point) as elev_ft, round(navaid.freq / 100.0,2) as freq
	FROM navaid
	JOIN nav_type ON nav_type.ntype_id = navaid.ntype_id;
	"""
    Cur.execute(sql)
    Con.commit()

    ## m_vpr # unused
    print "create view: `mv_vor`"
    sql = """
	CREATE OR REPLACE VIEW mv_vor AS
	SELECT  navaid.ident, navaid.name, navaid.ntype_id, nav_type.ntype,
	navaid.point,
	ST_Z(navaid.point) as elev_ft
	FROM navaid
	JOIN nav_type ON nav_type.ntype_id = navaid.ntype_id
	"""
    Cur.execute(sql)
    Con.commit()

    ## m_vpr # unused
    print "create view: `mv_wp`"
    sql = """
	CREATE OR REPLACE VIEW mv_wp AS
	SELECT  procedure_wp.point, procedure_wp.ident
	FROM procedure_wp

	"""
    Cur.execute(sql)
    Con.commit()
    print "create view: `mv_airport`"
    sql = """
    CREATE OR REPLACE VIEW mv_airport AS
    SELECT apt_ident, apt_name,  center
    FROM airport
    """
    Cur.execute(sql)
    Con.commit()

    print "create view: `mv_runway_line`"
    sql = """
    CREATE OR REPLACE VIEW mv_runway_line AS
    SELECT t0.ident as thr_ident_0, t1.ident as thr_ident_1, runway.surface_id,
    ST_MakeLine(t0.threshold, t1.threshold) as rwy_center_line
    FROM runway
    JOIN threshold t0 ON runway.thr0_id = t0.thr_id
    JOIN threshold t1 ON runway.thr1_id = t1.thr_id
    """
    Cur.execute(sql)
    Con.commit()

    print "create view: `mv_ils_line`"
    sql = """
    CREATE OR REPLACE VIEW mv_ils_line AS
    SELECT
    ST_MakeLine(threshold.loc_extent, rec.threshold) as ils_line
    FROM threshold
    inner join threshold rec on threshold.recip_id = rec.thr_id
    """
    Cur.execute(sql)
    Con.commit()

    print "create view: `mv_threshold`"
    sql = """
    CREATE OR REPLACE VIEW mv_threshold AS
    SELECT threshold.ident, abs(round(hdg,0)) as hdg, threshold.threshold
    FROM threshold

    """
    Cur.execute(sql)
    Con.commit()

    print "create view: `mv_apt_10`"
    sql = """
    CREATE OR REPLACE VIEW mv_apt_10 AS
    SELECT apt_range_10nm as geom
    FROM airport
    """
    Cur.execute(sql)
    Con.commit()

    print "create view: `mv_apt_30`"
    sql = """
    CREATE OR REPLACE VIEW mv_apt_30 AS
    SELECT apt_range_30nm as geom
    FROM airport
    """
    Cur.execute(sql)
    Con.commit()

    print "create view: `mv_im`"
    sql = """
    CREATE OR REPLACE VIEW mv_im AS
    SELECT
    im as point
    FROM threshold where im is not null
    """
    Cur.execute(sql)
    Con.commit()

    print "create view: `mv_mm`"
    sql = """
    CREATE OR REPLACE VIEW mv_mm AS
    SELECT
    mm as point
    FROM threshold where mm is not null
    """
    Cur.execute(sql)
    Con.commit()


    print "create view: `mv_om`"
    sql = """
    CREATE OR REPLACE VIEW mv_om AS
    SELECT
    om as point
    FROM threshold where om is not null
    """
    Cur.execute(sql)
    Con.commit()
