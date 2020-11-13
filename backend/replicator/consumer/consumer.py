from kafka import KafkaConsumer
import mysql.connector
import json
import uuid
import argparse
import logging

parser = argparse.ArgumentParser()


parser.add_argument("host")
parser.add_argument("port")
parser.add_argument("user")
parser.add_argument("password")
parser.add_argument("bootstrap")
parser.add_argument("topic")

args = parser.parse_args()

db = mysql.connector.connect(host=args.host, port=args.port, user=args.user, passwd=args.password)
dbp = db.cursor()
consumer = KafkaConsumer(args.topic, bootstrap_servers=args.bootstrap, group_id='secure-suite')

logging.info('Waiting for kafka events...')

try:
  for msg in consumer:
    message = {"key": json.loads(msg.key), "value": json.loads(msg.value)}
    database_name = message["key"]["database"]
    table_name = message["key"]["table"]
    event_type = message["value"]["type"]
    timestamp = message["value"]["ts"]
    xid = message["value"]["xid"]
    data = message["value"]["data"]
    logging.info("EVENT Database: {}, Table: {}, Event Type: {}, Data: {}".format(database_name, table_name, event_type, data))
    
    dbp.execute("use audit")
    dbp.execute("CREATE TABLE IF NOT EXISTS {}_events (`event_key` VARCHAR(36) NOT NULL, `table` VARCHAR(255) NOT NULL, `column` VARCHAR(255), `data` VARCHAR(255), `event_type` VARCHAR(50) NOT NULL,  `xid` VARCHAR(255) NOT NULL, `timestamp` VARCHAR(255), PRIMARY KEY (`event_key`))".format(database_name))

  for c, v in data.items():
    dbp.execute("INSERT INTO `{}_events` VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(database_name, str(uuid.uuid4()), table_name, c, v, event_type, xid, timestamp))

except Exception as e:
  logging.error(e)

