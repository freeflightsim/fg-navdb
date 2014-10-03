
package navdb

import (
	"fmt"

	"net/url"
	//_ "github.com/lib/pq"
	"database/sql"
)



func SearchAll(DB *sql.DB, query url.Values) (NavResultsPayload, error) {

	res := NewNavResultsPayload()

	params := ParseParams(query)
	fmt.Println(params)

	//# Get all the airports.. TODO if in ntype
	airports, err_apt := DB_SearchAirports(DB, params)
	if err_apt != nil {

	}
	for _, apt := range airports {
		//fmt.Println(idx, apt)
		nrec := NavRec{}
		nrec.NType = apt.NType
		nrec.Ident = apt.Ident
		nrec.Name = apt.Name
		nrec.Lat = apt.Lat
		nrec.Lon = apt.Lon
		nrec.ElevM = apt.ElevM
		nrec.ElevFt = apt.ElevFt
		res.AddNavRec(nrec)
	}

	//#Get all anvaids


	
    return res,  nil
	
}
