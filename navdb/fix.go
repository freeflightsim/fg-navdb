
package navdb

import (
	//"os"
    //"path/filepath"
	//"io/ioutil"
	"fmt"
	//"bufio"
	//"strings"
	//"strconv"
	//"github.com/revel/revel"
	//_ "github.com/lib/pq"
	//"database/sql"
)

// THis is a Job i want to fire as a one off
type Import_FixDatJob struct {}
func (j Import_FixDatJob) Run() {
	//Import_FixDat()
}
/*
func Import_FixDat() {
	
	file_path := "/home/fgxx/fgx-navdata/temp/xplanezip" + "/earth_fix.dat"
	
	file, err := os.Open(file_path)
	if err != nil {
		fmt.Fprintf(os.Stderr, "The file %s does not exist!\n", file_path)
		return
	}
	defer file.Close()

	c := 0
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		c += 1
		line :=  scanner.Text() 
		//fmt.Println("<", c, line)
		if c < 4 {
			continue
		}
		//parts := strings.Split(strings.TrimSpace(line), " ")
		var err1, err2 error
		n := NavRec{}
		n.ElevM = -9999
		n.ElevFt = -9999
		//n := NavAid{}
		n.Lat, err1 = strconv.ParseFloat(strings.TrimSpace(line[:10]), 32)
		n.Lon, err2 = strconv.ParseFloat(strings.TrimSpace(line[12:22]), 32)
		
		//n.Lat = strings.TrimSpace(line[:10])
		//n.Lon = strings.TrimSpace(line[12:22])
		n.Ident = strings.TrimSpace(line[23:])
		if err1 != nil || err2 != nil {
			fmt.Println(">", c, line, err1, err2)
		}
		//kwargs['fix_center'] = ut.mk_point(lon=kwargs['lon'], lat=kwargs['lat'], alt=0)
		Fixp := MkGeom(n)
		fmt.Println(Fixp)

		sql := "insert into navaid("
		sql += "ident, name, search, ntype_id, point "
		sql += ") values("
		sql += "$1, $2,  $3, 201, $4 )"
		_, errd := DB.Exec(sql, n.Ident, n.Ident, n.Ident, MkGeom(n))
		if  errd != nil {
			fmt.Println(errd)
			//return 
		}
		if c == 20 {
			break
		}
	}	
	 
}
*/

// Creates a `POINT()`m or `POINTZ()` if altitude set
func MkPoint(nav NavRec) string {
	//if nav.Alt != None:
	//W	return "" //POINTZ(%s %s %s)" %(lon, lat, alt)
	return fmt.Sprintf("POINTZ(%f %f %d)", nav.Lon, nav.Lat, nav.ElevFt)
}

func MkGeom(nav NavRec) string {
	//if nav.Alt != None:
	//W	return "" //POINTZ(%s %s %s)" %(lon, lat, alt)
	p := MkPoint(nav)
	return fmt.Sprintf("ST_Transform(ST_GeomFromText('%s', 4326),3857))", p)
}
