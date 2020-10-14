set global binlog_format=ROW;
set global binlog_row_image=FULL;

CREATE USER 'secure_suite'@'%' IDENTIFIED BY 'IWANTTOBEHACKED';
GRANT ALL ON secure_suite.* TO 'secure_suite'@'%';

CREATE USER 'maxwell'@'%' IDENTIFIED BY 'maxwell';
GRANT ALL ON maxwell.* TO 'maxwell'@'%';
GRANT SELECT, REPLICATION CLIENT, REPLICATION SLAVE ON *.* TO 'maxwell'@'%';

CREATE DATABASE secure_suite;

