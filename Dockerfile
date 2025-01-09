FROM python:3.11-slim-bullseye

ENV POLLING=True
ENV COOKIE_PATH=config/cookies.txt

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

CMD python main.py
