package main

import (
	"net/http"
    "github.com/labstack/echo"
)

func main() {
	e := echo.New()
	var u Updator
    e.GET("/", func(c echo.Context) error {
		deploymentName := c.QueryParam("deploymentName")
		newImageName := c.QueryParam("newImageName")
		u.UpdateDeploymentImage(deploymentName, newImageName)
        return c.String(http.StatusOK, "OK")
    })

	e.Logger.Fatal(e.Start(":80"))
	
	
}