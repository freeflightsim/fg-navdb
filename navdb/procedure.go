package navdb

import (
	"fmt"
	"database/sql"

	//"strings"
	//"net/url"
	"github.com/revel/revel"

)



// The nav rec is a general structure used
// to represent airports, fix and navaids
type Procedure struct{
	ProcId int64 `json:"proc_id"`
	AptIdent string `json:"apt_ident"`
	NType string `json:"ntype"`
	Ident string `json:"ident"`
	Name string `json:"name"`
	WayPoints []ProcedureWp `json:"waypoints"`
}

type ProcedureWp struct{
	//WpId int64 `json:"wp_id"`
	WpNo int `json:"wp_no"`
	//Name string `json:"apt_ident"`
	//Ident string `json:"ident"`
	Ident string `json:"ident"`

	//Freq string `json:"freq"`
	//Hz string
	Lat float64 `json:"lat"`
	Lon float64 `json:"lon"`

	//ElevM int `json:"elev_m"`
	AltFt int `json:"alt_ft"`
	AltRestrict string `json:"alt_restriction"`
}

func DB_GetSids(DB *sql.DB, apt_ident string) (map[string]Procedure, error) {

	lst :=  make(map[string]Procedure, 0)

	sql := "SELECT proc_id, apt_ident, ntype, ident  "
    sql += " from v_procedure "
	sql += " where apt_ident= '" + apt_ident + "' "
	sql += " and ntype ='sid'  "
	sql += " order by ident asc "

	fmt.Println(sql)
	rows, err := DB.Query(sql)
    if err != nil {
		revel.ERROR.Println(err)
        return nil,  err
    }
	defer rows.Close()

	for rows.Next(){
		ob := Procedure{}
		err := rows.Scan( &ob.ProcId, &ob.AptIdent, &ob.NType,  &ob.Ident)
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			//lst = append(lst, ob)
			lst[ob.Ident] = ob
		}

	}
    return lst,  nil
}

func DB_GetStars(DB *sql.DB, apt_ident string) (map[string]Procedure, error) {

	lst :=  make(map[string]Procedure, 0)

	sql := "SELECT proc_id, apt_ident, ntype, ident  "
    sql += " from v_procedure "
	sql += " where apt_ident= '" + apt_ident + "' "
	sql += " and ntype ='star'  "
	sql += " order by ident asc "

	fmt.Println(sql)
	rows, err := DB.Query(sql)
    if err != nil {
		revel.ERROR.Println(err)
        return nil,  err
    }
	defer rows.Close()

	for rows.Next(){
		ob := Procedure{}
		err := rows.Scan( &ob.ProcId, &ob.AptIdent, &ob.NType,  &ob.Ident)
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			//lst = append(lst, ob)
			var err_wp error
			ob.WayPoints, err_wp = GetWayPoints(DB, ob.ProcId)
			if err_wp != nil {

			}
			lst[ob.Ident] = ob
		}

	}
    return lst,  nil
}

func GetWayPoints(DB *sql.DB, proc_id int64) ([]ProcedureWp, error) {

	lst :=  make([]ProcedureWp, 0)

	sql := "SELECT wp_no, ident, lat, lon, alt_ft, alt_restriction  "
    sql += " from v_procedure_wp "
	sql += " where proc_id =  $1 "
	sql += " order by wp_no asc "
	fmt.Println(sql)
	rows, err := DB.Query(sql, proc_id)
    if err != nil {
		revel.ERROR.Println(err)
        return nil,  err
    }
	defer rows.Close()

	for rows.Next(){
		ob := ProcedureWp{}
		err := rows.Scan( &ob.WpNo, &ob.Ident, &ob.Lat,  &ob.Lon, &ob.AltFt, &ob.AltRestrict)
		if err != nil {
            revel.ERROR.Println(err)
        } else {
			//lst = append(lst, ob)
			fmt.Println(ob)
			lst = append(lst, ob)
		}

	}
    return lst,  nil
}
