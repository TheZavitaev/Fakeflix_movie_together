FROM python:3.9-slim as build
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libssl-dev gettext locales git libpq-dev && \
    echo ru_RU.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen && apt-get autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN find /opt/venv -name 'pycache' -exec rm -Rf {} +

WORKDIR /app/
COPY / /app/

ENTRYPOINT [ "./scripts/entrypoint.sh" ]
