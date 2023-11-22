CREATE database if not exists aart;
USE aart;
DROP TABLE art;
CREATE TABLE art 
(
	id INT PRIMARY KEY AUTO_INCREMENT,
	title TEXT,
	art TEXT,
	userid INT,
	karma INT DEFAULT 0
);

DROP TABLE users;
CREATE TABLE users
(
	id INT PRIMARY KEY AUTO_INCREMENT,
	username TEXT,
	password TEXT
);

DROP TABLE privs;
CREATE TABLE privs
(
	userid INT PRIMARY KEY,
	isRestricted BOOL
);
