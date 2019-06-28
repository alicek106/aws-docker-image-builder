FROM golang:1.12.6-alpine
RUN apk add git
RUN git clone https://github.com/alicek106/aws-docker-image-builder.git
WORKDIR aws-docker-image-builder/cd-server
RUN go build
CMD ["./hello"]
