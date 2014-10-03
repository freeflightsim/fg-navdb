
package controllers

import (
    //"fmt"
    "github.com/fgx/fg-navdb/navdb"
	"github.com/fgx/fg-navdb/app"
	"github.com/revel/revel"
)

type NavAid struct {
    *revel.Controller
}



type NavaidSearchPayload struct {
	Success bool `json:"success" xml:"success"`
	Rows []navdb.NavRec `json:"rows" xml:"rows"`
	Src string `json:"src" xml:"src"`
	Message string `json:"message" xml:"message"`
	Error string `json:"error" xml:"error"`
}

//= Returns airports search /json/airports?query
func (c NavAid) SearchJson() revel.Result {

	data := new(NavaidSearchPayload)
	data.Success = true

	var err error
	data.Rows,  err = navdb.DB_SearchNavaids(app.DB, c.Params.Query)
	
	if err != nil {
		revel.TRACE.Println(err)
	}
    return c.RenderJson(data)
}
