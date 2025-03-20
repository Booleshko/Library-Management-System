FROM python:3.11-slim
LABEL maintainer="bohdan.oleshko0@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR / library_service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
