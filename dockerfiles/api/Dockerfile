FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

ARG ROOT_APP=/app

COPY movie_together/app/requirements.txt $ROOT_APP/requirements.txt

WORKDIR $ROOT_APP

RUN pip install --upgrade pip setuptools wheel
RUN pip --no-cache-dir install asyncpg
RUN pip --no-cache-dir install httptools

RUN pip install -r requirements.txt

COPY movie_together/app/src $ROOT_APP/

CMD uvicorn main:app --port 8000 --host 0.0.0.0