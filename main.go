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
	port := ":443"
	proxy1 := os.Getenv("PROXY_ONE")
	proxy2 := os.Getenv("PROXY_TWO")
        fmt.Printf("(proxy1: %v \nproxy2: %v\n", proxy1, proxy1)

	// go StartLogServer("server1", port1)
	// go StartLogServer("server2", port2)

	main_server := http.NewServeMux()
	// handle all requests to your server using the proxy
	main_server.HandleFunc("/", ProxyRequestHandler(proxy1, proxy2))
	fmt.Printf("started main server on port: %s \n", port)
	log.Fatal(http.ListenAndServeTLS(port, "cert.pem", "key.pem", main_server))
}

// ProxyRequestHandler handles the http request using proxy
func ProxyRequestHandler(proxy1, proxy2 string) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
                fmt.Printf("new request")
		body, _ := ioutil.ReadAll(r.Body)
		buf1 := ioutil.NopCloser(bytes.NewBuffer(body))
		buf2 := ioutil.NopCloser(bytes.NewBuffer(body))
		_, err := http.Post(proxy1, "application/json", buf1)
		if err != nil {
			fmt.Println(err)
		}
		_, err = http.Post(proxy2, "application/json", buf2)
		if err != nil {
			fmt.Println(err)
		}
		w.Write([]byte("ok"))
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

