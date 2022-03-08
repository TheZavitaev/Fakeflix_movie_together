FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

ARG ROOT_APP=/app

COPY movie_together/mock_auth/requirements.txt $ROOT_APP/requirements.txt

WORKDIR $ROOT_APP

RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt

COPY movie_together/mock_auth/src $ROOT_APP/
