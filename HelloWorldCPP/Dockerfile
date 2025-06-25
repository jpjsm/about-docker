FROM alpine:3.18.0
RUN apk add build-base
COPY helloworld.cpp /opt/HelloWorld/
WORKDIR /opt/HelloWorld/
RUN g++ -o HelloWorld helloworld.cpp
CMD ["./HelloWorld"]