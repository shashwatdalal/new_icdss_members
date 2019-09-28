FROM alpine:3.10
RUN apk add --update python3 python3-dev gfortran py3-pip build-base
RUN pip3 install seaborn
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
