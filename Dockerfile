FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY app/requirements.txt requirements.txt
COPY /app /app

EXPOSE 5000

RUN pip install --no-cache-dir --upgrade -r requirements.txt

