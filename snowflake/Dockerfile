FROM golang

WORKDIR /go/src/goldflake

ADD . .

RUN go get github.com/AmreeshTyagi/goldflake@latest

CMD ["go", "run", "main.go"]

EXPOSE 8080
