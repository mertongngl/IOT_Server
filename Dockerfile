FROM python:3.5

ADD . /api

WORKDIR /api

RUN pip install -r requirements.txt

RUN export FLASK_APP=api.py

ENTRYPOINT [ "python", "api.py" ]