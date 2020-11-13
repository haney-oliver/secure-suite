set global binlog_format=ROW;
set global binlog_row_image=FULL;

CREATE USER 'secure_suite'@'%' IDENTIFIED BY 'IWANTTOBEHACKED';
GRANT ALL ON secure_suite.* TO 'secure_suite'@'%';

CREATE USER 'maxwell'@'%' IDENTIFIED BY 'maxwell';
GRANT ALL ON maxwell.* TO 'maxwell'@'%';
GRANT SELECT, REPLICATION CLIENT, REPLICATION SLAVE ON *.* TO 'maxwell'@'%';

CREATE DATABASE secure_suite;

CREATE TABLE IF NOT EXISTS secure_suite.user(
  user_key VARCHAR(36) UNIQUE NOT NULL,
  user_name VARCHAR(255) UNIQUE NOT NULL,
  user_password TEXT NOT NULL,
  user_email VARCHAR(255) UNIQUE NOT NULL,
  user_salt VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_key)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS secure_suite.session(
  session_key VARCHAR(36) UNIQUE NOT NULL,
  ref_user_key VARCHAR(36) UNIQUE NOT NULL,
  locked_out BOOLEAN DEFAULT 0,
  PRIMARY KEY (session_key),
  FOREIGN KEY (ref_user_key) REFERENCES secure_suite.user(user_key)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS secure_suite.category(
  category_key VARCHAR(36) UNIQUE NOT NULL,
  ref_user_key VARCHAR(36) NOT NULL,
  category_name VARCHAR(255) UNIQUE NOT NULL,
  category_description TEXT NOT NULL,
  PRIMARY KEY (category_key),
  FOREIGN KEY (ref_user_key) REFERENCES secure_suite.user(user_key)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS secure_suite.password(
  password_key VARCHAR(36) UNIQUE NOT NULL,
  ref_user_key VARCHAR(36) NOT NULL,
  ref_category_key VARCHAR(36) NOT NULL,
  password_content VARCHAR(255) NOT NULL,
  password_username VARCHAR(255) NOT NULL,
  password_url TEXT NOT NULL,
  PRIMARY KEY (password_key),
  FOREIGN KEY (ref_user_key) REFERENCES secure_suite.user(user_key),
  FOREIGN KEY (ref_category_key) REFERENCES secure_suite.category(category_key)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS secure_suite.url(
  url_key VARCHAR(36) UNIQUE NOT NULL,
  ref_user_key VARCHAR(36) NOT NULL,
  url_string TEXT NOT NULL,
  url_tokens TEXT NOT NULL,
  url_sequence TEXT NOT NULL,
  url_good BOOLEAN NOT NULL DEFAULT 0,
  PRIMARY KEY (url_key),
  FOREIGN KEY (ref_user_key) REFERENCES secure_suite.user(user_key)
) ENGINE=InnoDB;
