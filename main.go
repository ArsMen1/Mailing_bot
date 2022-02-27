package main

import (
	"bytes"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	port := flag.String("port", ":443", "port where to start server with colon: ex :443")
	proxy1 := flag.String("proxy1", "", "proxy target 1")
	proxy2 := flag.String("proxy2", "", "proxy target 2")

	flag.Parse()

	if *proxy1 == "" || *proxy2 == "" {
		panic("proxy targets uset")
	}

	// go StartLogServer("server1", port1)
	// go StartLogServer("server2", port2)

	main_server := http.NewServeMux()
	// handle all requests to your server using the proxy
	main_server.HandleFunc("/", ProxyRequestHandler(*proxy1, *proxy2))
	fmt.Printf("started main server on port: %s \n", *port)
	log.Fatal(http.ListenAndServeTLS(*port, "cert.pem", "key.pem", main_server))
}

// ProxyRequestHandler handles the http request using proxy
func ProxyRequestHandler(proxy1, proxy2 string) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
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
