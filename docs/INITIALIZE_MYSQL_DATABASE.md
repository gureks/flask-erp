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
	
3. Create `profile` table:
	```	mysql> CREATE TABLE profile(
				username VARCHAR(100) NOT NULL,
				name VARCHAR(100) NOT NULL,
				dob DATE,
				sex ENUM('Male','Female') NOT NULL,
				email VARCHAR(100),
				address VARCHAR(100),
				number VARCHAR(20),
				PRIMARY KEY(username)
			   );
		mysql> INSERT INTO profile
				VALUES ('admin','Administrator God', '2017-04-15', 'Male', 'gurek15033@iiitd.ac.in', 'IIIT-Delhi, Okhla Estate III', '9910004979');	   
	```
