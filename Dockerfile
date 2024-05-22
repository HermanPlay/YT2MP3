FROM python:3.11-slim-bullseye

ENV POLLING=True

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

CMD python bot.py