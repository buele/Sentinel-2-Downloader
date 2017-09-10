# ==================================================================================== #
#
# Copyright (c) 2017  Raffaele Bua (buele)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==================================================================================== #

FROM debian

# Create app directory
RUN mkdir -p /usr/downloader
RUN mkdir -p /usr/downloader/supervisord
RUN mkdir -p /urs/downloader/pip

# Update apt-get dependencies
RUN apt-get update
RUN  apt-get install -y --no-install-recommends apt-utils

#install python and pip
RUN apt-get install -qy python3.4
WORKDIR /usr/pip
RUN mkdir -p /usr/pip
COPY vendors/get-pip.py /usr/pip
RUN ls
RUN python3.4 get-pip.py
WORKDIR /usr

#install flask
RUN pip install Flask
RUN pip install -U flask-cors

#install wget
RUN apt-get install -y wget

# install sqlalchemy
RUN pip install sqlalchemy


RUN mkdir -p /usr/downloader/server

RUN export PYTHONPATH=${PYTHONPATH}:/usr/downloader
WORKDIR /usr/downloader/
RUN apt-get update
RUN apt-get install -qy python2.7
WORKDIR /usr/pip
RUN python2.7 get-pip.py
RUN python2.7 -m pip install supervisor

## install postgres
RUN apt-get update
RUN apt-get install -y  libpq-dev postgresql-client postgresql-client-common
RUN apt-get install -y  python3-psycopg2

##install crontab
RUN apt-get install -y cron
RUN apt-get install -y python3-crontab



WORKDIR /usr/downloader/




