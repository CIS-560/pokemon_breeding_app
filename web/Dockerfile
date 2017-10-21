FROM python:3.5
ENV PYTHONUNBUFFERED 1

ARG env

WORKDIR /app
ADD . /app
RUN pip install -r requirements/$env.txt
