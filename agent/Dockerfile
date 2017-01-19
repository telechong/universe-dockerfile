FROM ubuntu:16.04
MAINTAINER Jesper Derehag <jderehag@hotmail.com>

# numpy must be installed prior to universe!
RUN apt-get update; \
    apt-get upgrade -y; \
    apt-get dist-upgrade -y; \
    apt-get install git python python-pip golang libjpeg-turbo8-dev -y; \
    pip install --upgrade pip; \
    pip install numpy; \
    pip install opencv-python numpy scipy tensorflow universe six; \
    git clone https://github.com/jderehag/universe-starter-agent.git

EXPOSE 2222 12345
