FROM python:3.10-alpine

ARG APP_USER="consumer"
ARG APP_GROUP="consumer"
ARG APP_UID="1000"
ARG APP_GID="1000"
ARG APP_DIR="/app"

ENV PATH="${APP_DIR}/venv/bin:${PATH}"

RUN adduser -g "${APP_GID}" -u "${APP_UID}" -h "${APP_DIR}" "${APP_USER}" -D

RUN apk add curl & \
    apk add make automake g++ gcc python3 python3-dev gfortran linux-headers musl-dev build-base openblas-dev

USER "${APP_USER}"

WORKDIR "${APP_DIR}"

RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip3 install --upgrade pip setuptools wheel && \
    pip3 install kafka-python prometheus-client && \
    mkdir -p app

RUN pip3 install scipy

COPY ./source app
COPY docker-entrypoint.sh .

ENTRYPOINT ["/bin/sh", "docker-entrypoint.sh"]