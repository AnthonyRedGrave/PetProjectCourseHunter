FROM python:3.9.4-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./fastapi_core/ .
COPY ./admin/ .
COPY . .
