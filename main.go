package main

import (
	//"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"os"
)

func main() {

	file, err := ioutil.ReadFile("polls.json")
	if err != nil {
		fmt.Printf("File error: %v\n", err)
		os.Exit(1)
	}

	testString := string(file)
	fmt.Println(testString)
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		fmt.Println("endpoint hit")
		c.String(200, testString)
	})

	r.Run(":8080")
}
