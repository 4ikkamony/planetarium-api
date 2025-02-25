FROM python:3.13-alpine

WORKDIR /usr/src/

COPY ./requirements requirements

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/dev.txt

WORKDIR /usr/src/app/

COPY ./src/ .

COPY ./commands /usr/src/commands

RUN apk update && apk add --no-cache dos2unix

RUN dos2unix /usr/src/commands/*.sh

RUN adduser --disabled-password --no-create-home django-user

RUN mkdir -p /usr/src/app/media/uploads/ \
    && chown -R django-user:django-user /usr/src/app/media/ \
    && chmod -R 755 /usr/src/app/media/ \
    && chmod -R +x /usr/src/commands/ \
    && chmod -R 777 /usr/src/app

USER django-user
