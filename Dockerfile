FROM python:3.8.3-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

ADD main.py event.py database.py requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]