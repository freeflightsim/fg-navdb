package controllers

import (
	//"fmt"
	//"encoding/xml"
	"github.com/revel/revel"
	"github.com/fgx/fg-navdb/app"
	"github.com/fgx/fg-navdb/navdb"
	
	
)



type NavDb struct {
	*revel.Controller
}


// /json/all
func (c NavDb) SearchAllJson() revel.Result {

	data, err := navdb.SearchAll(app.DB, c.Params.Query)
	if err != nil {
		
	}
	
	return c.RenderJson(data)
}

// /json/ntypes
func (c NavDb) NTypesJson() revel.Result {

	data, err := navdb.SearchAll(app.DB, c.Params.Query)
	if err != nil {
		
	}
	
	return c.RenderJson(data)
}

//==========================================================================================
// Legacy FgMap
// navdata search fg_nav_xml.cgi?
func (c NavDb) FGMapNavXml() revel.Result {

	
	data, err := navdb.GetFgMapXml(app.DB, c.Params.Query)
	if err != nil {
		
	}
	return c.RenderXml(data)

}
