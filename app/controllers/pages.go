package controllers

import (
	//"fmt"
	
	
	"github.com/revel/revel"
	"github.com/fgx/fg-navdb/navdb"
	
	// TODO markdown
	//"github.com/russross/blackfriday"
	//"os"
	//"io/ioutil"
	//"errors"
)
/*
 TODO MARKDOWN
 
func GetFileContents(file_path string) ([]byte, error) {
	full_path := revel.BasePath + file_path
	if _, err := os.Stat(full_path); os.IsNotExist(err) {
		return nil, errors.New( "No such file: " +  file_path )
	}
	txt, err_read := ioutil.ReadFile(full_path) 
	return txt, err_read
}

func GetMarkDown(file_name string) (string, error) {
	txt, err := GetFileContents( "/app/views/pages/" + file_name + ".md" )
	if err != nil {
		return "", err
	}
	html := blackfriday.MarkdownCommon(txt)
	return string(html), nil
}
*/
type Pages struct {
	*revel.Controller
}

func (c Pages) Index() revel.Result {
	return c.Render()
}

func (c Pages) JsonApi() revel.Result {
	return c.Render()
}
func (c Pages) KmlApi() revel.Result {
	return c.Render()
}
func (c Pages) XmlApi() revel.Result {
	return c.Render()
}
func (c Pages) OtherApi() revel.Result {
	return c.Render()
}

func (c Pages) Sources() revel.Result {
	
	//content, _ := GetMarkDown("sources")
	
	return c.Render()
}

func (c Pages) Widget() revel.Result {

	return c.Render()
}


func (c Pages) IconsCss() revel.Result {

	css := navdb.GetIconsCss()
	c.Response.ContentType = "text/css"
	return c.RenderText(css)
}