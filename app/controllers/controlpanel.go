package controllers

import (
	"strings"
    "github.com/fgx/fg-navdb/navdb"
	"github.com/fgx/fg-navdb/app"
	"github.com/revel/revel"
	//"github.com/revel/revel/modules/jobs/app/jobs"
)

type ControlPanel struct {
    *revel.Controller
}

func (c ControlPanel) Index() revel.Result {
	
	
	return c.Render()
}





// ====================================================================
type RoutesInfoPayload struct {
	Success bool `json:"success"`
	Routes []RouteInfo `json:"routes"`
}
type RouteInfo struct {
	Url string `json:"url"`
	Controller string `json:"controller"`
	Action string `json:"action"`
}
// Handle the routes view - only return /json/* and /xml/* adn /kml/*
func (c ControlPanel) RoutesJson(table string) revel.Result {
	
	data := new(RoutesInfoPayload)
	data.Success = true
	
	data.Routes = make([]RouteInfo,0)
	for _, r := range revel.MainRouter.Routes {
		if strings.HasPrefix(r.Path, "/xml/") || strings.HasPrefix(r.Path, "/json/") || strings.HasPrefix(r.Path, "/kml/") {
			data.Routes = append(data.Routes, RouteInfo{Url:r.Path, Controller: r.ControllerName, Action: r.Action} )
		}
	}
	
	return c.RenderJson(data)
}

// ====================================================================
/*
type DBInfoPayload struct {
	Success bool `json:"success"`
	Views []navdb.DB_TableInfo `json:"views,omitempty"`
	Tables []navdb.DB_TableInfo `json:"tables,omitempty"`
}
*/

// Returns all db info
func (c ControlPanel) DB_InfoJson() revel.Result {
	
	data, err := navdb.DB_GetTablesAndViewsPayload(app.DB)
	if err != nil {
		revel.ERROR.Println(err)
	}
	return c.RenderJson(data)
}

// Returns views
func (c ControlPanel) DB_ViewsJson() revel.Result {
	
	data, err := navdb.DB_GetViewsPayload(app.DB)
	if err != nil {
		revel.ERROR.Println(err)
	}
	return c.RenderJson(data)
}

// Returns tables
func (c ControlPanel) DB_TablesJson() revel.Result {
	data, err := navdb.DB_GetTablesPayload(app.DB)
	if err != nil {
		revel.ERROR.Println(err)
	}
	return c.RenderJson(data)
}


// ====================================================================
// Returns data on a table
func (c ControlPanel) DB_TableJson(table string) revel.Result {
	
	data, err := navdb.DB_GetTablePayload(app.DB, table)
	if err != nil {
		revel.ERROR.Println(err)
	}
	return c.RenderJson(data)
}


// return data on a view
func (c ControlPanel) DB_ViewJson(table string) revel.Result {
	
	data, err := navdb.DB_GetViewPayload(app.DB, table)
	if err != nil {
		revel.ERROR.Println(err)
	}
	return c.RenderJson(data)
}
/*

func (c ControlPanel) DB_ViewUpdateJson(table string) revel.Result {
	
	data := new(DBViewPayload)
	data.Success = true
	
	
	err := navdb.DB_UpdateView(table)
	if err != nil {
		revel.ERROR.Println(err)
	}
	
	data.Table, err = navdb.DB_GetView(table)

	if err != nil {
		revel.ERROR.Println(err)
	}

	return c.RenderJson(data)
}
*/









//= Starts the ImportFix dat import
/*
func (c ControlPanel) ImportFixDatJson() revel.Result {
	
	data := new(navdb.DB_TablePayload)
	data.Success = true
	
	//jobs.Now( navdb.Import_FixDatJob{} )
	
	//go navdb.Import_FixDat()
	

	return c.RenderJson(data)
}
*/
