FROM python:3.7-slim-stretch

USER root

ADD . /

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8050

ENV NAME World

CMD ["python", "Dash_App.py"]