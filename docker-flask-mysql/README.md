To check available mysql images
```
docker search mysql
```

To pull the latest mysql images
```
docker pull mysql
docker image ls
```

To start the mysql container
```
docker run -itd --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

Goes to the container of mysql
```
docker container ls
docker exec -ti <container_id> /bin/bash
mysql -h localhost -u root -p
```

Basic command of mysql
```
SHOW databases;
CREATE DATABASE techbow;
USE techbow;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    PRIMARY KEY ( `id` ),
    INDEX NAME_IND (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SHOW tables;
DESC user;
INSERT INTO user (name, email) VALUES ("A", "a@gmail.com");
SELECT * FROM user WHERE name = 'A';



CREATE TABLE IF NOT EXISTS `product` (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `product_name` VARCHAR(20) NOT NULL,
    `supplier` VARCHAR(20) NOT NULL,
    `price` INT UNSIGNED,
    PRIMARY KEY ( `id` ),
    INDEX NAME_IND (product_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SHOW tables;
DESC product;
INSERT INTO product (product_name, supplier, price) VALUES ("coke", "amazon", 1);
SELECT * FROM product WHERE product_name = 'coke';



CREATE TABLE IF NOT EXISTS `user_product` (
    `user_id` INT UNSIGNED,
    `product_id` INT UNSIGNED,
    CONSTRAINT user_product_pk PRIMARY KEY (user_id, product_id),
    CONSTRAINT FK_user FOREIGN KEY (user_id) REFERENCES user (id),
    CONSTRAINT FK_product FOREIGN KEY (product_id) REFERENCES product (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SHOW tables;
DESC user_product;
INSERT INTO user_product (user_id, product_id) VALUES (1, 1);
SELECT * FROM user_product;
```

To build the image contains the web app
```
docker build -t web-mysql:v1 .
```

To check the image we just build
```
docker image ls
```

Deploy a docker contains the web app.
```
docker run -p 5001:5001 --link mysql:mysql-host -d --name web-mysql web-mysql:v1
```

Check the host setting in webapp from docker container.
```
docker exec -ti <container_id> /bin/bash
cat /etc/hosts
```
