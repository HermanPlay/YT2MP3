FROM continuumio/anaconda3:latest

ENV POLLING=True

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

RUN conda create -n virtualenv python=3.11 -y

COPY requirements.txt .

RUN conda run -n virtualenv --no-capture-output pip install -r requirements.txt

COPY src .

CMD conda run -n virtualenv --no-capture-output python bot.py