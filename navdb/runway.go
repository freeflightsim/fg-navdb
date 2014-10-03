
package navdb

import (
	//"strings"
	//"time"
	//"fmt"
	//"github.com/revel/revel/cache"
	//"database/sql"
	//"net/url"
	"github.com/revel/revel"
	//_ "github.com/lib/pq"
	"database/sql"
)



type Runway struct {
	Rwy string `json:"runway" db:"runway"  xml:"runway"`
	
	LengthM float32 `json:"length_m" db:"length_m" xml:"length_m"`
	
	CenterLat float32 `json:"center_lat" db:"elev_ft" xml:"center_lat"`
	CenterLon float32 `json:"center_lon" db:"elev_ft" xml:"center_lon"`
	
	ThrIdent0 string `json:"thr_ident_0" db:"thr0_ident" xml:"thr_ident_0"`
	StartLat0 float32 `json:"start_lat_0" db:"start0_lat" xml:"start_lat_0"`
	StartLon0 float32 `json:"start_lon_0" db:"start0_lon" xml:"start_lon_0"`
	DisplacedM0 float32 `json:"displaced_m_0" db:"displacement0_m" xml:"displaced_m_0"`
	ThrLat0 float32  `json:"thr_lat_0" db:"thr0_lat" xml:"thr_lat_0"`
	ThrLon0 float32  `json:"thr_lon_0" db:"thr0_lon" xml:"thr_lon_0"`
	
	ThrIdent1 string `json:"thr_ident_1" db:"thr1_ident" xml:"thr_ident_1"`
	StartLat1 float32 `json:"start_lat_1" db:"start1_lat" xml:"start_lat_1"`
	StartLon1 float32 `json:"start_lon_1" db:"start1_lon" xml:"start_lon_1"`
	DisplacedM1 float32 `json:"displaced_m_1" db:"displacement1_m" xml:"displaced_m_1"`
	ThrLat1 float32  `json:"thr_lat_1" db:"thr1_lat" xml:"thr_lat_1"`
	ThrLon1 float32  `json:"thr_lon_1" db:"thr1_lon" xml:"thr_lon_1"`
	
	ElevFt int  `json:"elev_ft" db:"elev_ft" xml:"elev_ft"`
	ElevM int `json:"elev_m" db:"elev_m" xml:"elev_m"`
}



func DB_GetRunways(DB *sql.DB, ident string)([]Runway, error) {
    
	lst :=  make([]Runway, 0)
	// TODO cache here
	
	sql := "SELECT rwy, "
    sql += " center_lat, center_lon, length_m,"
    sql += " thr0_ident, start0_lat, start0_lon, displacement0_m,  thr0_lat, thr0_lon, "
    sql += " thr1_ident, start1_lat, start1_lon, displacement1_m,  thr1_lat, thr1_lon "
    sql += " from v_runway "    
    sql += " where apt_ident = $1 "
	sql += " order by rwy asc "
	
	rows, err := DB.Query(sql, ident)
    if err != nil {
		revel.ERROR.Println(err)
        return nil,  err
    }
	defer rows.Close()

	for rows.Next(){
		ob := Runway{}
		err := rows.Scan( 	&ob.Rwy, &ob.CenterLat, &ob.CenterLon,  &ob.LengthM,
							&ob.ThrIdent0, &ob.StartLat0, &ob.StartLon0, &ob.DisplacedM0, &ob.ThrLat0, &ob.ThrLon0, 
							&ob.ThrIdent1, &ob.StartLat1, &ob.StartLon1, &ob.DisplacedM1, &ob.ThrLat1, &ob.ThrLon1)
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			lst = append(lst, ob)
		}
       
	}
	return lst, nil
}
