FROM alpine:3.10

RUN apk add --update python3 python3-dev gfortran py3-pip build-base aws-cli
RUN pip3 install seaborn requests
