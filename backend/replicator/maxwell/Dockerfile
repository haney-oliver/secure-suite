FROM openjdk:latest

WORKDIR /

ADD ./maxwell/maxwell-1.27.1/ /maxwell-1.27.1/
ADD ./wait-for-it.sh /maxwell-1.27.1

WORKDIR /maxwell-1.27.1/

CMD ./wait-for-it.sh ${HOST}:3306 -t 45 -- bin/maxwell --user=${USER} --password=${PASSWORD} --host=${HOST} --producer=kafka --kafka.bootstrap.servers=${BOOTSTRAP_SERVERS} --kafka_topic=${TOPIC} --jdbc_options=${JDBC_OPTIONS} --filter="exclude: secure_suite.alembic_version"

