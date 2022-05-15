# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster
WORKDIR /app
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN git clone https://github.com/cruf99/ChannelChat.git
WORKDIR ChannelChat
RUN pip3 install -r requirements.txt
COPY ${CONFIG} .
CMD [ "python3", "-m", "channelchat"]