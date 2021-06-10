package main

import (
    "github.com/go-kit/kit/endpoint"
    "github.com/go-kit/kit/log"
    httptransport "github.com/go-kit/kit/transport/http"
    "net/http"
    "os"
)

type loggingMiddleware struct {
    logger log.Logger
    next   StringService
}

func main() {
    logger := log.NewLogfmtLogger(os.Stderr)

	svc := stringService{}

	var uppercase endpoint.Endpoint
	uppercase = makeUppercaseEndpoint(svc)
	uppercase = loggingMiddleware(log.With(logger, "method", "uppercase")) (uppercase)

	var count endpoint.Endpoint
	count = makeCountEndpoint(svc)
	count = loggingMiddleware(log.With(logger, "method", "count")) (count)

	uppercaseHandler := httptransport.NewServer(
		uppercase,
		decodeUppercaseRequest,
		encodeResponse)
	countHandler := httptransport.NewServer(
		count,
		decodeCountRequest,
		encodeResponse)
	http.Handle("/uppercase", uppercaseHandler)
	http.Handle("/count", countHandler)
	http.ListenAndServe(":8080", nil)
}


