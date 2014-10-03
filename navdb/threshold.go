
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







type Threshold struct{
	
	AptIdent string `json:"apt_ident"`
	ThrIdent string `json:"thr_ident"`
	
	StartLat float64
	StartLon float64
	
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


func DB_GetThresholds(DB *sql.DB, ident string)(map[string]Threshold, error) {
    
	lst :=  make(map[string]Threshold, 0)
	// TODO cache here
	
    sql := "SELECT ident, "
    sql += " start_lat, start_lon, displacement_m,  threshold_lat, threshold_lon, "
		//sql += " om_lat, om_lon, mm_lat, mm_lon, im_lat, im_lon, "
    sql += " loc_point_lat,  loc_point_lon, loc_extent_lat,  loc_extent_lon "
    // #sql += "  gs_point0_lat,  gs_point0_lon, gs_point1_lat,  gs_point1_lon "
    sql += " from v_threshold " 
    sql += " where apt_ident = $1 "
	
	rows, err := DB.Query(sql, ident)
    if err != nil {
		revel.ERROR.Println(err)
        return nil,  err
    }
	defer rows.Close()

	for rows.Next(){
		ob := Threshold{}
		err := rows.Scan( 	&ob.ThrIdent, 
							&ob.StartLat, &ob.StartLon, &ob.DisplacedM, &ob.ThrLat, &ob.ThrLon,
							//&ob.OmLat, &ob.OmLon,  &ob.MmLat, &ob.MmLon, &ob.ImLat, &ob.ImLon,  
							&ob.LocLat, &ob.LocLon, &ob.LocExtentLat, &ob.LocExtentLon)
						
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			lst[ob.ThrIdent] = ob
		}
       
	}
	return lst, nil
}



