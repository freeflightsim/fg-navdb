
package navdb

import (
	//"os"
    //"path/filepath"
	//"io/ioutil"
	//"fmt"
	"sort"
	//"bufio"
	//"strings"
	//"strconv"
	//"github.com/revel/revel"
	//"github.com/revel/revel/cache"
	//"github.com/fgx/fg-navdb/app"
	//"net/url"
	//"github.com/fgx/fg-navdb/app"
)

// The main NavType definition
var NTypes = map[string]string {
	"apt" : "Airport",
	"rwy" : "Runway",
	"thr" : "Theshold",

	"ils" : "ILS",
	"om"  : "Outer Marker",
	"mm"  : "Middle Marker",
	"im"  : "Inner Marker",

	"fix" : "Fix",

	"vor" : "VOR",
	"dme" : "Distance measuring equipment",

	"ndb" : "Non Directional Beacon",
	
	"ifr" : "Instrument Flight Rules",
	"vfr" : "Visual Flight Rules",
}

// return a list of the ntype.s sorted as array
func GetNTypes() []string {
	mk := make([]string, len(NTypes))
    i := 0
    for k, _ := range NTypes {
        mk[i] = k
        i++
    }
    sort.Strings(mk)
	return mk
}

// Check whether this ki exists
func IsValidNType(ki string) bool {
	
	if _, ok := NTypes[ki]; ok {
		return true
	}	
	return false
}

