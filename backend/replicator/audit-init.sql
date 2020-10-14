CREATE USER 'maxwell_consumer'@'%' IDENTIFIED BY 'maxwell_consumer';
CREATE DATABASE audit;
GRANT ALL ON audit.* TO 'maxwell_consumer'@'%';
