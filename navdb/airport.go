
package navdb

import (
	"strings"
	//"time"
	"fmt"
	//_ "github.com/lib/pq"
	"database/sql"
	"net/url"
	"github.com/revel/revel"
	//"github.com/fgx/fg-navdb/app"
)


// The Airport is consisted of runways and other bits
type Airport struct{
	//#AptPK uint64 //'json:null' // database
	
	NType string `json:"ntype" db:"ntype"  xml:"ntype"`
	// The ICAO Pilots Code for this airport eg EGLL 
	Ident string `json:"ident" db:"ident" xml:"ident"`

	// Descriptive Name eg London Heathrow
	Name string `json:"name" db:"name" xml:"name"`
	
	// The airport name for passengers
	//Iata string `json:"iata"`
		
	Lat float64 `json:"lat" db:"lat" xml:"lat"`
	Lon float64 `json:"lon" db:"lon" xml:"lon"`
		
	// The Runways are an array 
	//Runways []*Runway `json:"runways"`
	
	ElevFt int  `json:"elev_ft" db:"elev_ft" xml:"elev_ft"`
	ElevM int `json:"elev_m" db:"elev_m" xml:"elev_m"`
	
	// The ATC comms will be also
	//Comms [] *string `json:"comms"` //## TODO
}



func DB_AllAirports(DB *sql.DB)([]Airport, error) {
    
	lst :=  make([]Airport, 0)
	
	/*
	ki := "airports_all"
	errc := cache.Get(ki, &airports);
	if errc != nil 	{
		return airports, "cache", nil
	}
		fmt.Println(errc)
	*/
    sql := "SELECT 'apt' as ntype, apt_ident as ident, apt_name as name, elev_m, elev_ft, center_lat as lat, center_lon as lon "
    sql += " from v_airport "
    sql += " order by apt_ident asc "
	//fmt.Println(sql)
	
	rows, err := DB.Query(sql)
    if err != nil {
		revel.ERROR.Println(err)
        return nil,  err
    }
	defer rows.Close()

	for rows.Next(){
		ob := Airport{}
		err := rows.Scan( &ob.NType, &ob.Ident, &ob.Name, &ob.ElevM, &ob.ElevFt, &ob.Lat, &ob.Lon )
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			lst = append(lst, ob)
		}
       
	}

    //return data, nil
    /*
    err := app.DB.Select(&airports, sql)
    if err != nil {
		fmt.Println(err)
        return airports, "sb", err
    }
    */
    //fmt.Println(lst)
	//go cache.Set(ki, airports, 1 * time.Minute)
	
    return lst,  nil
    
}
func SearchAirports(DB *sql.DB, query url.Values)([]Airport, error) {
	
	params := ParseParams(query)
	return DB_SearchAirports(DB, params)
}

//func DB_SearchAirports(query url.Values)([]Airport, error) {
func DB_SearchAirports(DB *sql.DB, params SearchParams)([]Airport, error) {
    
	
	
	lst :=  make([]Airport, 0)
	
	
	sql := "SELECT 'apt' as ntype, apt_ident as ident, apt_name as name, elev_m, elev_ft, center_lat as lat, center_lon as lon "
    sql += " from v_airport "
	sql += " where 1 = 1 "
	
	sqlvars := make([]interface{},0)
	/*
    sqlvars = {}
    
    sql = "SELECT 'apt' as ntype, apt_ident as ident, apt_name as name, elev_m, elev_ft, center_lat as lat, center_lon as lon "
    sql += " from v_airport "
    sql += " where 1 = 1 "
    
    */
    // find by ident
    switch params.Action {
		
		case S_IDENT:
			sql += " and apt_ident like '%" + params.Ident + "%' "
        

		case S_SEARCH:
			/*
			#print "src=", params.search
			parts = ut.xsplit(params.search, upper=True)
			sql += " and ("
			for idx, p in enumerate(parts):
				if idx >  0:
					sql += " and "
				var_name = "search_%s" % idx
				sql += " apt_search like %(" + var_name + ")s "
				sqlvars[var_name] = "%" + p + "%"
			sql += ") "
			*/
			sql += " and ("
			for idx,snippet := range params.Search {
				if idx > 0 {
					sql += " and "
				}
				sql += " apt_search like '%" + snippet + "%' "
			}
			sql += ") "
		
		
		case S_BBOX:
			sql += " and center && ST_Transform(ST_MakeEnvelope(" + params.BBox + ", 4326), 3857)"
		
		// return nothing
		default:
		
			sql += " and apt_pk = 0 "
			return lst, nil
	}   
    sql += " order by apt_ident asc "
    sql += " limit 200; "

	
	fmt.Println(sql)
	fmt.Println(sqlvars)
	rows, err := DB.Query(sql, sqlvars...)
    if err != nil {
		revel.ERROR.Println(err)
        return nil,  err
    }
	defer rows.Close()

	for rows.Next(){
		ob := Airport{}
		err := rows.Scan( &ob.NType, &ob.Ident, &ob.Name, &ob.ElevM, &ob.ElevFt, &ob.Lat, &ob.Lon )
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			lst = append(lst, ob)
		}
       
	}
	
    return lst,  nil
    
}


func DB_GetAirport(DB *sql.DB, ident string)(Airport, error) {
    
	var ob Airport
    
	sql := "SELECT 'apt' as ntype, apt_ident as ident, apt_name as name, elev_m, elev_ft, center_lat as lat, center_lon as lon "
    sql += " from v_airport "
	sql += " where apt_ident = $1 "
    sql += " limit 1 "
	
	revel.INFO.Println(ident, sql)
	err := DB.QueryRow(sql, ident).Scan( &ob.NType, &ob.Ident, &ob.Name, &ob.ElevM, &ob.ElevFt, &ob.Lat, &ob.Lon )
	if err != nil {
		return ob, err
	}
	return ob, nil
	
}


type AirportData struct {
	Success bool `json:"success" xml:"success"`
	Ident string `json:"ident" xml:"ident"`
	Airport Airport `json:"airport" xml:"airport"`
	Runways []Runway `json:"runways" xml:"runways"`
	Thresholds map[string]Threshold `json:"thresholds" xml:"thresholds"`

	Sids map[string]Procedure `json:"sids" xml:"thresholds"`
	Stars map[string]Procedure `json:"stars" xml:"thresholds"`

	Error string `json:"error" xml:"error"`
	//Success bool `json:"success"`
	//Success bool `json:"success"`
	
}
func (me *AirportData) AddError(err error) {
	me.Error += err.Error() + "\n"
}
	
	


func GetAirport(DB *sql.DB, ident string) (AirportData) {
	
	var err error
	data := AirportData{Ident: ident}
	
	data.Ident = strings.ToUpper( strings.TrimSpace(ident) )
	if len(data.Ident) < 4 {
		data.Error = "Ident is too short"
		return data
	}
	
	
	
	
	data.Airport, err = DB_GetAirport(DB, data.Ident)
	if err != nil {
		data.AddError(err)
		//return data, err
	}
	
	data.Runways, err = DB_GetRunways(DB, data.Ident)
	if err != nil {
		data.AddError(err)
	}
	
	data.Thresholds, err = DB_GetThresholds(DB, data.Ident)
	if err != nil {
		data.AddError(err)
	}

	data.Sids, err = DB_GetSids(DB, data.Ident)
	if err != nil {
		data.AddError(err)
	}

	 data.Stars, err = DB_GetStars(DB, data.Ident)
	if err != nil {
		data.AddError(err)
	}

	return  data
}


