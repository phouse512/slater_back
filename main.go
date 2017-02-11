package main

import (
	//"encoding/json"
	"database/sql"
	"fmt"
	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
	"io/ioutil"
	"os"
)

var (
	id int
)

func main() {

	db, err := sql.Open("postgres", "postgres://phil:3YToxjG2hj3wYoWKc84a2AYYEBiiABTa@piper.phizzle.space/piperdb")

	if err != nil {
		fmt.Printf("error: %v\n", err)
	}

	test_query, err := db.Query("SELECT id from commit_log limit 10")
	if err != nil {
		fmt.Printf("query failed: %v\n", err)
	}

	defer test_query.Close()
	for test_query.Next() {
		err := test_query.Scan(&id)
		if err != nil {
			fmt.Printf("error: %v\n", err)
		}
		//		fmt.Printf("id: %v", id)
	}

	file, err := ioutil.ReadFile("polls.json")
	if err != nil {
		fmt.Printf("File error: %v\n", err)
		os.Exit(1)
	}

	pollString := string(file)

	file, err = ioutil.ReadFile("leaderboard.json")
	if err != nil {
		fmt.Printf("File error: %v\n", err)
		os.Exit(1)
	}

	leaderString := string(file)

	// initialize gin server
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		fmt.Println("endpoint hit")
		c.String(200, pollString)
	})

	r.GET("/leaderboard", func(c *gin.Context) {
		fmt.Println("leaderboard endpoint")
		c.String(200, leaderString)
	})

	r.Run(":8080")
}
