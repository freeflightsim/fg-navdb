package navdb

var LocalIcons = map[string]string {
	
	"icoFgx":  "fgx-cap-16.png",
	"icoFlightGear":  "flightgear_icon.png",
	
	"icoAirport":  "apt.png",
	"icoFix":  "vfr_fix.png",
	"icoNdb":  "ndb.16.png",
	"icoVor":  "vor.png",
	"icoDme":  "dme.png",
	"icoClr":  "go.gif",
}

var FamFamIcons = map[string]string {
	"icoAirways":  "chart_line.png",
	"icoFlightPlans":  "page_white_actionscript.png",
	
	"icoHelp":  "help.png",
	"icoExecute":  "accept.png",
	"icoHtml":  "html.png",
	
	"icoDev":  "shape_align_bottom.png",
	"icoDatabase":  "database.png",
	
	"icoSelectStyle":  "color_swatch.png",
	
	"icoLogin":  "key.png",
	
	"icoRefresh":  "refresh.gif",
	
	"icoOn":  "bullet_pink.png",
	"icoOff":  "bullet_black.png",


	"icoBookMarkAdd":  "book_add.png",
	
	"icoSettings":  "cog.png",
	
	"icoCallSign":  "page_white_c.png",
	
	
	"icoFlights":  "text_horizontalrule.png",
	
	"icoMapCore":  "map.png",
	"icoMap":  "map.png",
	"icoMapAdd":  "map_add.png",
	"icoMapGo":  "map_go.png",
	
	"icoMpServers":  "server_database.png",
	
	"icoBlue":  "bullet_blue.png",
	"icoOrange":  "bullet_orange.png",
	"icoPink":  "bullet_pink.png",
	"icoGreen":  "bullet_green.png",
	"icoRed":  "bullet_red.png",
	"icoWhite":  "bullet_white.png",
	"icoYellow":  "bullet_yellow.png",


	"icoUsers":  "group.png",
	"icoUser":  "user.png",
	"icoUserAdd":  "user_add.png",
	"icoUserEdit":  "user_edit.png",
	"icoUserDelete":  "user_delete.png",


	"icoRoutes":  "arrow_switch.png",

	"icoCancel":  "bullet_black.png",
	"icoSave":  "accept.png",
	
	
	
	
	"icoRefreshStop":  "clock_stop.png",
	"icoRefreshRun":  "clock_run.png",

}

func GetIconsCss() string {
	
	s := ""
	
	for k, v := range LocalIcons {
		s += "." + k + "{background-image: url('/public/img/" + v + "') !important; background-repeat: no-repeat;}\n" 
	}
	s += "\n\n" 
	
	for k, v := range FamFamIcons {
		s += "." + k + "{background-image: url('http://static.freeflightsim.org/icons/famfam_silk/" + v + "') !important; background-repeat: no-repeat;}\n"
	}
	s += "\n\n" 
	
	
	return s
}
