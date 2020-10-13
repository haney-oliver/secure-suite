FROM tensorflow/tensorflow:latest

WORKDIR /

ADD app/ app/
ADD requirements.txt requirements.txt
ADD replicator/wait-for-it.sh ./app/wait-for-it.sh

RUN apt-get install -y libmysqlclient-dev
RUN pip3 install --upgrade pip
RUN pip3 install Flask Flask-Cors Flask-SQLAlchemy Flask-Migrate keras SQLAlchemy mysqlclient


WORKDIR /app/


CMD ["bash", "-c", "./wait-for-it.sh mysql:3306 -t 60 -- python3 app.py"]

