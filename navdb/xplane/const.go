
package xplane

import (	
	
	//"fmt"
	//"strings"
	//"sort"
	//"regexp"
	
	//"os"
	//"bufio"
	//"io/ioutil"
	
)

type XPlaneBlob struct {
	FileName string `json:"file_name"`
	Series string `json:"series"`
	Dated string `json:"dated"`
	Ariac string `json:"ariac"`
	Nick string `json:"nick"`
	DataUrl string `json:"data_url"`
}

func NewXplaneBlob() {
	
}