package controllers

import (
    //"fmt"
	"github.com/fgx/fg-navdb/app"
    "github.com/fgx/fg-navdb/navdb"
	"github.com/revel/revel"
)

type Airport struct {
    *revel.Controller
}



type AirportLookupPayload struct {
	Success bool `json:"success" xml:"success"`
	Rows []navdb.Airport `json:"rows" xml:"rows"`
	Src string `json:"src" xml:"src"`
	Message string `json:"message" xml:"message"`
}


//===================================================================================
// Airports
//===================================================================================



//= Returns all airports /json/airports/all
func (c Airport) AllJson() revel.Result {

	
	payload := new(AirportLookupPayload)
	payload.Success = true
	
	var err error
    payload.Rows,  err = navdb.DB_AllAirports(app.DB)
	
	if err != nil {
		revel.TRACE.Println(err)
	}
    return c.RenderJson(payload)
}


//= Returns airports search /json/airports?query
func (c Airport) SearchJson() revel.Result {

	
	data := new(AirportLookupPayload)
	data.Success = true

	
	var err error
	data.Rows,  err = navdb.SearchAirports(app.DB, c.Params.Query)
	
	if err != nil {
		revel.TRACE.Println(err)
	}
    return c.RenderJson(data)
}

//===================================================================================
// Airport
//===================================================================================

func (c Airport) AirportHandler(ident, ext string) revel.Result {

	data := navdb.GetAirport(app.DB, ident)	
	switch ext {
		case "json":
			return c.RenderJson(data)
		
		case "xml":
			return c.RenderXml(data)
	}
	return c.Render(data)
}


func (c Airport) Airport(ident string) revel.Result {

	data := navdb.GetAirport(app.DB, ident)		
    return c.Render(data)
}

func (c Airport) AirportJson(ident string) revel.Result {

	data := navdb.GetAirport(app.DB, ident)	
    return c.RenderJson(data)
}


func (c Airport) AirportXml(ident string) revel.Result {
	
	return c.Render()
}




