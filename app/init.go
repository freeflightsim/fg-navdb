package app

import (
	"os"
	"fmt"
	
	_ "github.com/lib/pq"
	"database/sql"
	
	"github.com/revel/revel"
	
	"github.com/fgx/fg-navdb/navdb"
)

func init() {
	// Filters is the default set of global filters.
	revel.Filters = []revel.Filter{
		revel.PanicFilter,             // Recover from panics and display an error page instead.
		revel.RouterFilter,            // Use the routing table to select the right Action
		revel.FilterConfiguringFilter, // A hook for adding or removing per-Action filters.
		revel.ParamsFilter,            // Parse parameters into Controller.Params.
		revel.SessionFilter,           // Restore and write the session cookie.
		revel.FlashFilter,             // Restore and write the flash cookie.
		revel.ValidationFilter,        // Restore kept validation errors and save new ones from cookie.
		revel.I18nFilter,              // Resolve the requested language
		AddAllowCORSHeaders,           // Add CORS
		revel.InterceptorFilter,       // Run interceptors around the action.
		revel.CompressFilter,          // Compress the result.
		revel.ActionInvoker,           // Invoke the action.
	}

	// register startup functions with OnAppStartOpen
	// ( order dependent )
	revel.OnAppStart(InitDB)
	// revel.OnAppStart(FillCache())
}


// all origins
var AddAllowCORSHeaders = func(c *revel.Controller, fc []revel.Filter) {
	
	// todo: Only add these to /json/* /xml/*
	
	c.Response.Out.Header().Add("Access-Control-Allow-Origin", "*")
	c.Response.Out.Header().Add("Access-Control-Allow-Methods", "GET, OPTIONS")
	c.Response.Out.Header().Add("Access-Control-Allow-Headers", "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token")
	
	fc[0](c, fc[1:]) // Execute the next filter stage.
}


func checkError(err error, s string) {
    // Syslogger
    //logger, _ := syslog.New(syslog.LOG_ERR, "SyncServer")
    //defer logger.Close()

    if err != nil {
            //logger.Err(fmt.Sprintf("%s: %s", s, err))
            panic(fmt.Sprintf("%s: %s", s, err))
    }
}

//==============================================================================
// out shared config in json wit others apps..
// wish revel would do something about this
//==============================================================================

//==============================================================================
// DataBase Load
//==============================================================================
var DB *sql.DB


func InitDB() {
	
	//read config.json
	
	
	conf, errc := navdb.LoadConfig(revel.BasePath)
	if errc != nil {
		fmt.Println("OOPS", errc)
		os.Exit(0)
	}
	//fmt.Println("BASE=", conf)
	revel.INFO.Println("Loaded config")
	cred := fmt.Sprintf("postgres://%s:%s@%s/%s?sslmode=disable", conf.DbLive.User, conf.DbLive.Password, conf.DbLive.Server, conf.DbLive.Database)
	var err error
	DB, err = sql.Open("postgres", cred)
	if err != nil {
		fmt.Println("err", err)
	}
	//connstring := fmt.Sprintf("user=%s password='%s' dbname=%s sslmode=disable", "fgxx", "foobar", "fgxmap")
	//var err error
    //DB, err = sqlx.Connect("postgres", connstring)
    //checkError(err, "sqlx.Open")
	revel.INFO.Println("DB Connected")
    return 
	
}


