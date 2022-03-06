FROM python:3.9-buster

WORKDIR /app
COPY api/requirements.txt .
RUN pip install -r requirements.txt

COPY utils/wait_for_kafka.py /

COPY ./compose/api/production/start /
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./api/src src
