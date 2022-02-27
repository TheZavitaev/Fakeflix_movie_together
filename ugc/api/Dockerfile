FROM python:3.9-buster

WORKDIR /app
COPY api/requirements.txt .
RUN pip install -r requirements.txt
COPY ./api/src src

COPY utils/wait_for_kafka.py /

WORKDIR /app/src
CMD python /wait_for_kafka.py && gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker