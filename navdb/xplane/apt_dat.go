
package xplane

import (	
	
	"fmt"
	"strings"
	"sort"
	"regexp"
	
	"os"
	"bufio"
	"io/ioutil"
	
	"github.com/fgx/fg-navdb/navdb"
)

const (
	
	FILE_PERMS = 0777
	
	// ROW_CODES
	RC_AIRPORT = "1"
	RC_SEAPORT = "16"
	RC_HELIPORT = "17"
	
	
)

var APT_ICAO_MATCH = regexp.MustCompile("[A-Z]{4}")


	
// SPEC = http://data.x-plane.com/file_specs/XP%20APT1000%20Spec.pdf
// The aiports are a block of text with a blank line as delimiter
// This creates a []list of lines for each block, eg
/*
1      298 0 1 M64  Ball
100   45.72   3   0 0.25 0 0 0 18   33.87678797 -088.72378670    0.00    0.00 1  0 0 0 36   33.86955091 -088.72409108    0.00    0.00 1  0 0 0
19   33.87717763 -088.72302648 1 WS
19   33.86916125 -088.72485122 1 WS

1      571 0 0 YBAL Balladonia
100   49.99   4   0 0.25 0 0 0 13  -32.34285394  123.61018661    0.00    0.00 0  0 0 0 31  -32.35255900  123.62182400    0.00    0.00 0  0 0 0
100   34.14   4   0 0.25 0 0 0 4   -32.34907324  123.61269244    0.00    0.00 0  0 0 0 22  -32.34260146  123.61925844    0.00    0.00 0  0 0 0
*/
func ShardAptDat(conf navdb.Config) {
	
	fmt.Println("Shard_apt_dat", conf)
	
	file_path := conf.XPlaneZip + "/apt.dat"
	
	file, err := os.Open(file_path)
	if err != nil {
		fmt.Fprintf(os.Stderr, "The file %s does not exist!\n", file_path)
		return
	}
	defer file.Close()

	apt_index := make([]string, 0) // airport codes index
	
	lines := make([]string, 0) // the lines of the airport data
	c := 0 // line counter
	
	// scan the file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		
		c += 1 // increment line no
		
		line :=  strings.TrimSpace( scanner.Text() ) //read line
		
		if c < 4 {  // ignore first 4 lines
			continue
		}
		
		if len(line) > 0 {
			lines = append(lines, line)
			
		} else {
			apt_code, ok := ProcessAirportLines(conf, lines)
			if ok {
				apt_index = append(apt_index, apt_code)
				fmt.Println("SAVEd: ", c, apt_code  )
			}
			lines = make([]string, 0)
			
		}
	
		
		
		//if c == 4000 {
		//	WriteAptDatIndex(workspace_path, apt_index)
		//	os.Exit(0)
		//}

	}
	WriteAptDatIndex(conf, apt_index)
	
}

func WriteAptDatIndex(conf navdb.Config, apt_index []string) error {
	
	file_path := conf.StashDir + "/airport/index.txt"
	sort.Strings(apt_index)
	err := ioutil.WriteFile(file_path, []byte(strings.Join(apt_index, "\n")), FILE_PERMS)
	if err != nil {
		return err
	}
	fmt.Println("WROTE iNDEX", file_path)
	return nil
}

// return /E/G/L from EGLL
func GetAirportDirPath(apt_code string) string {
	p := strings.Split(apt_code, "")
	return "/airport/" + p[0] + "/" + p[1] + "/" + p[2] 
}

func WriteAptDatBlob(workspace_path, apt_code string, lines []string ) error {
	
	apt_dir := workspace_path + GetAirportDirPath(apt_code)
	err_mk := os.MkdirAll(apt_dir, FILE_PERMS)
	if err_mk != nil {
		//fmt.Println(err_mk)
		return err_mk
	}
	file_path := apt_dir + "/" + apt_code + ".xplane.10.txt"
	//fmt.Println(file_path)
	err := ioutil.WriteFile(file_path, []byte(strings.Join(lines, "\n")), FILE_PERMS)
    if err != nil {
		//fmt.Println(err)
		return err
	}
	return nil
}

func ProcessAirportLines(conf navdb.Config, lines []string) (string, bool) {
	//fmt.Println("SaveAirportLines: ", len(lines) )
	if len(lines) == 0 {
		return "", false
	}
	apt_row_code := strings.Split(lines[0], " ")[0]
	//fmt.Println("apt_row_code: ", apt_row_code )
	if apt_row_code == RC_AIRPORT {
		
		
		
		apt_code := strings.TrimSpace( lines[0][15:19] )
		is_icao := APT_ICAO_MATCH.MatchString(apt_code)
		if is_icao {
			WriteAptDatBlob(conf.StashDir, apt_code, lines)
			
			return apt_code, true
		}
		
		
	} else {
		fmt.Println("Ignore: ", lines[0])
		
	}
	return "", false
}