#!/bin/sh

python3 scripts/wait_for_kafka.py
python3 scripts/create_topics.py

exec "$@"
