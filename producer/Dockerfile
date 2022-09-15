FROM python:3.10-alpine3.16

ARG APP_USER="consumer"
ARG APP_GROUP="consumer"
ARG APP_UID="1000"
ARG APP_GID="1000"
ARG APP_DIR="/app"

ENV PATH="${APP_DIR}/venv/bin:${PATH}"

RUN adduser -g "${APP_GID}" -u "${APP_UID}" -h "${APP_DIR}" "${APP_USER}" -D

RUN apk add curl

USER "${APP_USER}"

WORKDIR "${APP_DIR}"

RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip3 install kafka-python prometheus-client && \
    mkdir -p app

COPY ./source app
COPY docker-entrypoint.sh .

ENTRYPOINT ["/bin/sh", "docker-entrypoint.sh"]