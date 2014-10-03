
package navdb

import (
	//"os"
    //"path/filepath"
	//"io/ioutil"
	"fmt"
	//"bufio"
	//"strings"
	"net/url"
	"github.com/revel/revel"
	//"github.com/revel/revel/cache"
	//_ "github.com/lib/pq"
	"database/sql"
)

type NavResultsPayload struct {
	Success bool `json:"success"`
	Rows []NavRec `json:"rows"`
}
func NewNavResultsPayload() NavResultsPayload {
	ob := NavResultsPayload{Success: true, Rows: make([]NavRec,0)}
	return ob
}

func (pl *NavResultsPayload) AddNavRec(rec NavRec){
	pl.Rows = append(pl.Rows, rec)
}


// The nav rec is a general structure used 
// to represent airports, fix and navaids
type NavRec struct{
	NType string `json:"ntype"`
	Ident string `json:"ident"`
	Name string `json:"name"`

	Freq string `json:"freq"`
	//Hz string
	Lat float64 `json:"lat"`
	Lon float64 `json:"lon"`
	
	ElevM int `json:"elev_m"`
	ElevFt int `json:"elev_ft"`
}



func DB_SearchNavaids(DB *sql.DB, query url.Values)([]NavRec, error) {

	params := ParseParams(query)

	lst := make([]NavRec, 0)

	sql := "SELECT ntype, ident, name, lat, lon, elev_m, elev_ft "
	sql += " from v_navaid "
	sql += " where 1 = 1 "

	if len(params.NTypes) > 0 {
		// add the ntypes filter
		sql += " and ("
		for idx, n := range params.NTypes {
			if idx > 0 {
				sql += " or "
			}
			sql += " ntype = '"+n+"' "
		}
		sql += ") "
	}
	
	
    switch params.Action {

		case S_BBOX:
			sql += " and point && ST_Transform(ST_MakeEnvelope(" + params.BBox + ", 4326), 3857)"

		case S_IDENT:
			sql += " and ident like '%" + params.Ident + "%' "
        
		case S_SEARCH:
			sql += " and ("
			for idx,snippet := range params.Search {
				if idx > 0 {
					sql += " and "
				}
				sql += " search like '%" + snippet + "%' "
			}
			sql += ") "
		


		default:
			sql += " and nav_id = 0 " // return nothing
			return lst, nil
	}   
    sql += " order by ident asc "
    sql += " limit 200; "

	fmt.Println(sql)
	rows, err := DB.Query(sql)
    if err != nil {
		revel.ERROR.Println(err)
        return nil,  err
    }
	defer rows.Close()

	for rows.Next(){
		ob := NavRec{}
		err := rows.Scan( &ob.NType, &ob.Ident, &ob.Name,  &ob.Lat, &ob.Lon, &ob.ElevM, &ob.ElevFt,)
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			lst = append(lst, ob)
		}
       
	}
    return lst,  nil
}
