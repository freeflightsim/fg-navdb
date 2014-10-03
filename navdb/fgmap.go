
package navdb

import (
	//"os"
    //"path/filepath"
	//"io/ioutil"
	"fmt"
	"encoding/xml"
	"github.com/revel/revel"
	//"github.com/revel/revel/cache"
	//"github.com/fgx/fg-navdb/app"
	"net/url"
	//_ "github.com/lib/pq"
	"database/sql"
)


//==========================================================================================
// Legacy FgMap
//==========================================================================================

type FGMapNaxAidsXml struct {
	XMLName xml.Name `xml:"navaids"`
	Airports []FGMapAirportXml `xml:"airport"`
	Count int `xml:"cnt,attr"`
	Debug string `xml:"debug,attr"`
}



type AirportThresholdScan struct{
	
	AptIdent string `json:"apt_ident"`
	AptName string `json:"apt_name"`
	
	ThrIdent string `json:"thr_ident"`
	
	StartLat float64  `json:"thr_lat" db:"start_lat"`
	StartLon float64  `json:"thr_lon" db:"start_lon"`
	
	DisplacedM float32 `json:"displaced_m" db:"displacement"`
	ThrLat float32  `json:"thr_lat" db:"thr_lat"`
	ThrLon float32  `json:"thr_lon" db:"thr_lon"`

	OmLat *float32  `json:"om_lat" db:"om_lat"`
	OmLon *float32  `json:"om_lon" db:"om_lon"`
	MmLat *float32  `json:"mm_lat" db:"mm_lat"`
	MmLon *float32  `json:"mm_lon" db:"mm_lon"`
	ImLat *float32  `json:"im_lat" db:"im_lat"`
	ImLon *float32  `json:"im_lon" db:"im_lon"`
	
	
	LocLat *float32  `json:"loc_lat" db:"loc_point_lat"`
	LocLon *float32 `json:"loc_lon" db:"loc_point_lon"`
	
	LocExtentLat *float32 `json:"loc_extent_lat" db:"loc_extent_lat"`
	LocExtentLon *float32  `json:"loc_extent_lon" db:"loc_extent_lon"`
	//Thresholds []*Threshold
	//Surface *Surface
}

type FGMapAirportXml struct {
	XMLName xml.Name `xml:"airport"`
	//Airport string `xml:"airport,attr"`
	Id int `xml:"id,attr"`
	Ident string `xml:"code,attr"`
	Name string `xml:"name,attr"`
	Elevation string `xml:"elevation,attr"`
	Heliport string `xml:"heliport,attr"`
	Seaport string `xml:"seaport,attr"`
	Runways []FGMapRunwayXml
}


func GetFgMapXml(DB *sql.DB, query url.Values) (FGMapNaxAidsXml, error) {	
	// create our custom search params
	params := SearchParams{}
	fmt.Println(query )
	
	data := FGMapNaxAidsXml{}
	data.Airports = make([]FGMapAirportXml,0)
	
	// fgmap uses no values ie ?sstr=amm&apt_code&apt_name&vor&ndb&fix&awy 
	// so check for existance of "var" in urlQuery
	for _, ki := range []string{"vor", "fix", "ndb", "foo"} {
		if _, ok := query[ki]; ok { // yes it exists
			if IsValidNType(ki) {
				params.AddNType(ki)
			}
		}
	}
	params.AddSearch(query.Get("sstr"))
	params.Action = S_SEARCH
	fmt.Println(params.NTypes, len(params.NTypes) )

	//== Get airports and thresholds
	sql := "SELECT  "
	sql += " v_airport.apt_ident, "
    sql += " v_threshold.ident, "
	sql += "v_threshold.start_lat, v_threshold.start_lon, v_threshold.displacement_m,  v_threshold.threshold_lat, v_threshold.threshold_lon, "
		//sql += " om_lat, om_lon, mm_lat, mm_lon, im_lat, im_lon, "
    sql += " v_threshold.loc_point_lat,  v_threshold.loc_point_lon, v_threshold.loc_extent_lat,  v_threshold.loc_extent_lon "
    // #sql += "  gs_point0_lat,  gs_point0_lon, gs_point1_lat,  gs_point1_lon "
    sql += " from v_threshold " 
	sql += " inner join v_airport on v_airport.apt_id = v_threshold.apt_id "
    sql += " where v_threshold.apt_ident like '%" + "EGL" + "%' "
	fmt.Println(sql)
	rows, err := DB.Query(sql)
    if err != nil {
		revel.ERROR.Println(err)
        return data,  err
    }
	defer rows.Close()
	
	// Now we have to loop around to get the "airports", and the "thresholds" = ruwnays
	// first we put allinto a map struct key by airport
	// then we serialise out to XML - umm
	apt_map := make( map[string]*FGMapAirportXml, 0)
	
	
	for rows.Next(){
		ob := AirportThresholdScan{}
		err := rows.Scan( 	&ob.AptIdent, &ob.AptName, 
							&ob.ThrIdent, 
							&ob.StartLat, &ob.StartLon, &ob.DisplacedM, &ob.ThrLat, &ob.ThrLon,
							//&ob.OmLat, &ob.OmLon,  &ob.MmLat, &ob.MmLon, &ob.ImLat, &ob.ImLon,  
							&ob.LocLat, &ob.LocLon, &ob.LocExtentLat, &ob.LocExtentLon)
						
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			apt, exists := apt_map[ob.AptIdent] 
			
			if exists == false {
				apt:= new(FGMapAirportXml)
				apt.Ident = ob.AptIdent
				apt.Name = ob.AptName
				apt_map[apt.Ident] = apt
			}
			rwy := FGMapRunwayXml{}
			rwy.ThrIdent = ob.ThrIdent
			rwy.Lat = ob.ThrLat
			rwy.Lon = ob.ThrLon
			apt.Runways = append(apt.Runways, rwy)
			
		}
       
	}

	return data, nil
	
}

type FGMapRunwayXml struct {
	ThrIdent string `xml:"num"`
	Lat float32 `xml:"lat"`
	Lon float32 `xml:"lon"`
	Heading string `xml:"heading"`
	Length string `xml:"length"`
	Width string `xml:"width"`
}