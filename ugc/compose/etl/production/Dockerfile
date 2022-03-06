FROM python:3.9-buster

COPY etl/requirements.txt .

RUN pip install -r requirements.txt

COPY utils/wait_for_kafka.py /

COPY ./compose/etl/production/start /
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./etl/src src
