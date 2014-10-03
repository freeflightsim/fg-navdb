
package xplane

import (	
	
	"fmt"
	"strings"
	//"sort"
	//"regexp"
	
	"os"
	"bufio"
	//"io/ioutil"
	
)

const (
		
)


// The navdata file is a whole bunch of rowcodes or various data types and approx 30k lines
// This creates a file of lines for each data type
func ShardNavDat(zip_path, workspace_path string) {
	
	fmt.Println("ShardNavDat", zip_path)
	
	file_path := zip_path + "/nav.dat"
	
	file, err := os.Open(file_path)
	if err != nil {
		fmt.Fprintf(os.Stderr, "The file %s does not exist!\n", file_path)
		return
	}
	defer file.Close()

	nfiles := make(map[string]*os.File, 0)
		
	c := 0 // line counter
	
	// scan the file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		
		c += 1 // increment line no
		
		line :=  strings.TrimSpace( scanner.Text() ) //read line
		
		if c < 4 {  // ignore first 4 lines
			continue
		}
		
		parts := strings.Split(line, " ")
		
		
		
		row_code := parts[0]
		if nfiles[row_code] == nil {
			file_name := workspace_path + "/navaids/nav." + parts[0] + ".txt"
			fmt.Println(file_name)
			var err_open error
			nfiles[row_code], err_open = os.Open(file_name)
			if err_open != nil {
				panic(err_open)
			}
		}
		
	}

	
}