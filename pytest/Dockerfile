FROM python:3

RUN pip install --upgrade pip && \
    pip install selenium pytest python-dateutil \
                rope flake8 autopep8

ENV TZ "Asia/Tokyo"

WORKDIR /docker-pytest