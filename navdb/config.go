
package navdb

import (
	//"os"
    //"path/filepath"
	"io/ioutil"
	//"fmt"
	"encoding/json"
	
)



type Config struct {
	Secret string `json:"secret"`
	WwwServer string `json:"www_server"`
	WwwPort string `json:"www_port"`
	DbLive ConfDbUser `json:"db_live"`
	DbStaging ConfDbUser `json:"db_staging"`
	StashDir string `json:"stash_dir"`
	XPlaneZip string `json:"xplane"`
}
type ConfDbUser struct {
	Server string `json:"server"`
	User string `json:"user"`
	Password string `json:"password"`
	Database string `json:"database"`
}

func LoadConfig(project_base_dir string) (Config, error) {
	
	conf := Config{}
	file_path := project_base_dir + "/conf/config.json"
	file, err := ioutil.ReadFile(file_path)
    if err != nil {
        //fmt.Printf("File error: %v\n", err)
        return conf, err
    }
    
    errj := json.Unmarshal(file, &conf)
    //fmt.Printf("Results: %v\n", conf)
	return conf, errj
}

