FROM python:3.7

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY ./data /app/data
COPY ./src /app/src
COPY ./.azureml /app/.azureml
COPY ./.env /app/.env
COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

