package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

func main() {
	port := ":5001"
	proxy1 := os.Getenv("PROXY_ONE")
	proxy2 := os.Getenv("PROXY_TWO")
        fmt.Printf("(proxy1: %v \nproxy2: %v\n", proxy1, proxy2)

	// go StartLogServer("server1", port1)
	// go StartLogServer("server2", port2)

	main_server := http.NewServeMux()
	// handle all requests to your server using the proxy
	main_server.HandleFunc("/", ProxyRequestHandler(proxy1, proxy2))
	fmt.Printf("started main server on port: %s \n", port)
	log.Fatal(http.ListenAndServe(port, main_server))
}

// ProxyRequestHandler handles the http request using proxy
func ProxyRequestHandler(proxy1, proxy2 string) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
                fmt.Println("new request")
                fmt.Println("_______________________")
		body, _ := ioutil.ReadAll(r.Body)
		fmt.Printf("%s \n", body)
		buf1 := ioutil.NopCloser(bytes.NewBuffer(body))
		buf2 := ioutil.NopCloser(bytes.NewBuffer(body))
		_, err := http.Post(proxy1, "application/json", buf1)
		if err != nil {
			fmt.Printf("proxy1 post: %v \n", err)
		}
		_, err = http.Post(proxy2, "application/json", buf2)
		if err != nil {
			fmt.Printf("proxy2 post: %v \n", err)
		}
		w.Write([]byte("ok"))
                fmt.Println("_______________________")
	}
}

// func StartLogServer(serverName, port string) {
// 	server := http.NewServeMux()
// 	server.HandleFunc("/", func(rw http.ResponseWriter, r *http.Request) {
// 		fmt.Printf("%v: %v \n", serverName, "hi")
// 	})
// 	fmt.Printf("started server: %s on port %s \n", serverName, port)
// 	log.Fatal(http.ListenAndServe(port, server))
// }

