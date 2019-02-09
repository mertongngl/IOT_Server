FROM python:3.5

ADD . /api

WORKDIR /api

RUN pip install -r requirements.txt

RUN export FLASK_APP=app.py

ENTRYPOINT [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]