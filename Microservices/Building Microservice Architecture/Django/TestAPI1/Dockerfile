FROM python:3.7-slim-stretch

MAINTAINER rahulkhatry4@gmail.com

LABEL description="First django image with Dockerfile."

COPY . /

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000