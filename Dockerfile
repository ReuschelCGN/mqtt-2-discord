FROM python:3.7
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Pre-reqs
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install --no-install-recommends -y python3-pip python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /usr/src/app && \
    mkdir /usr/src/app/logs
WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/