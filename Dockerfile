# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /ChannelChat
ENV CONFIG config.toml
COPY . .
RUN pip3 install -r requirements.txt
CMD python3 -m channelchat -c $CONFIG
