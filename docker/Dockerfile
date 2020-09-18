FROM python:3.8.2

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
#COPY . /usr/src/app/

ADD requirements /usr/src/requirements

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /usr/src/requirements/development.txt
