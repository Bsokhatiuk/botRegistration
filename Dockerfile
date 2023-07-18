FROM ubuntu:22.04

LABEL maintainer="Bohdan Sokhatiuk <b.sohatuykgmail.com>"

USER root

WORKDIR /home

COPY . .

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=Europe/Kiev \
    DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
    apt-get install apt-utils -y && \
    apt-get upgrade -y && \
    cat ./requirements.system | xargs apt-get install --no-install-recommends -y && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

