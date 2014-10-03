package navdb

import (
	"fmt"
	"strings"
	"net/url"
	//"github.com/revel/revel"
)
//= Search flags and used at SearchParams.Action
const (
	// Invalid action, ie incorrect vars or missing
	S_INVALID = "invalid"
	
	// Its a search
	S_SEARCH = "search"

	// Its a code or ident
	S_IDENT = "ident"
	
	// Its a bounding box
	S_BBOX = "bbox"
	
	// Its a center (and later to include range)
	S_CENTER = "center"
)



//TODO remove all illegal vars
func CleanStr(dirty string) string {
	
	s := strings.ToUpper( strings.TrimSpace( dirty ) )
	if s == "" {
		return s
	}
	chaos := ";:,.%&*"
	for idx, r := range chaos {
		s = strings.Replace(s, string(r), "", -1)
		fmt.Println(r, idx, string(r))
	}
	return s
}

func DoSplit(str string) []string {
	
	ret := make([]string,0)
	parts := strings.Split(str, ",")
	for _, p := range parts {
		tr := strings.TrimSpace(p)
		if tr != "" {
			ret = append(ret, tr)
		}
	}
	return ret
}



// These are the general search paramaters
type SearchParams struct {
	Ident string 	//?ident=foo
	Search[] string //?search=foo bar
	BBox string     //bbox=
	Center string   //?center=lat,lon
	Range_m int     //?range=20nm
	//Return[] string //todo - what data to return
	Action string  // the search action in order ident, search, bbox, center
	NTypes[] string // the ntypes to search (naily for navaids
	Format string  // the data dormat to return
}

// Add and ntype, TODO check and ignore dupes
func (me *SearchParams) AddNType(ntype string) {
	me.NTypes = append(me.NTypes, ntype)
}

// add query_string, split into parts and add to search array
func (me *SearchParams) AddSearch(query_str string) {
	search_str := strings.ToUpper( strings.TrimSpace( query_str ) )
	if search_str != "" {
		search_split := strings.Split(search_str, " ")
		for _, v := range search_split {
			if v != "" {
				me.Search = append(me.Search, v)
			}
		}
	}
}


// Load SearchParams and validate, ?search ?bbox or ?center must exist
// TODO relace invalid characters eg %
//TODO make all url query vars lower case
func ParseParams(query url.Values) SearchParams {
	
	p := SearchParams{}
	
	//TODO make all url query vars lower case
	/*
	for q in query {
		query[q] = lower(query[q])
	} */
	
	// ?search Is is a list of parts  eg "ea   lon  ro" = ["ea", "lon", "ro"]
	p.AddSearch( query.Get("search") )

	// ?ident=foo
	p.Ident = strings.ToUpper(strings.TrimSpace( query.Get("ident") ))	
	
	// TODO validate bbox
	p.BBox = strings.TrimSpace( query.Get("bbox") )
	
    p.Center = strings.TrimSpace( query.Get("center") )
	
	ntypes := strings.TrimSpace( query.Get("ntypes") )
	if ntypes != "" {
		narr := DoSplit(ntypes) 
		// Check navaid is valid
		for _, ki := range narr {
			if IsValidNType(ki) {
				p.AddNType(ki)
			}
		}
		
	}
	//fmt.Println(p.NTypes)
	// set validation flag
	if p.BBox  != "" {
		p.Action = S_BBOX

	}else if len(p.Search) > 2 {
		p.Action = S_SEARCH 
	
	}else if len(p.Ident) > 1  {
		p.Action = S_IDENT

		 
	} else if p.Center != "" {
		p.Action = S_CENTER
		 
	} else {
		p.Action = S_INVALID 
	}
	fmt.Printf("PARAMS=action=", p.Action, p)
	return p 
}
