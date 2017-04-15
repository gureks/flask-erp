# Steps to initialize MySQL Database

1. Create MySQL user:
	
	``` mysql -u <username> -p 
		Enter password:

		mysql> CREATE USER 'dbms'@'localhost' IDENTIFIED BY 'justanothersecret';
		mysql> GRANT ALL PRIVILEGES ON *.* TO 'dbms'@'localhost';
		mysql> FLUSH PRIVILEGES;
	```

2. Create database:
	```	mysql> CREATE DATABASE erp;
		mysql> USE erp;
	```	
		
3. Create `user` table:
	```	mysql> CREATE TABLE user(
				username VARCHAR(100) NOT NULL,
				password VARCHAR(100) NOT NULL,
				type ENUM('user','admin') NOT NULL,
				PRIMARY KEY(username)
			   );
		mysql> INSERT INTO user
				VALUES ('Admin','Admin','admin');	   
	```