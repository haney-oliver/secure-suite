FROM python:latest

WORKDIR /

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y build-essential

RUN pip3 install kafka-python
RUN pip3 install mysql.connector

ADD ./wait-for-it.sh /wait-for-it.sh
ADD ./consumer.py /consumer.py

CMD ./wait-for-it.sh ${AUDIT_DB_HOST}:${AUDIT_DB_PORT} -t 200 -- ./wait-for-it.sh ${KAFKA_HOST}:${KAFKA_PORT} -t 200 -- python3 consumer.py ${AUDIT_DB_HOST} ${AUDIT_DB_PORT} ${AUDIT_DB_USER} ${AUDIT_DB_PASSWORD} ${KAFKA_HOST}:${KAFKA_PORT} ${KAFKA_TOPIC}

