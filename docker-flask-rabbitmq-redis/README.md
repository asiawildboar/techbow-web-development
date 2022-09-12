## Objectvie
 - learn the basic knowledge of rabbitmq
 - pull rabbitmq image and bring up the docker container
 - connect rabbitmq to producer and consumer
 - producer: flask with restful api
 - consumer: flask with redis
 - introduce docker-compose

## Step 1: Set up RabbitMQ

### Bring up RabbitMQ
Reference: https://www.rabbitmq.com/download.html

pull the RabbitMQ docker image, get the Management plugin pre-installed.
```
docker pull rabbitmq:3.9-management
```
Bring up RabbitMQ. We’ll map port 15672 for the management web app and port 5672 for the message broker.

```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 -d rabbitmq:3.9-management
```

### Monitoring
Assuming that ran successfully, you've got an instance of RabbitMQ running! Bounce over to http://localhost:15672 to check out the management web app.

Log in using the default username (guest) and password (guest) and explore the management app a little bit. Here you can see an overview of your RabbitMQ instance and the message broker’s basic components: Connections, Channels, Exchanges, and Queues.

## Step 2: Set up Producer
Reference: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

### Bring up Producer 
```
docker build -t producer:v1 .
```

To run the flask app in docker and open browser at localhost:5001 to view the web app
```
docker run -p 5001:5001 --link rabbitmq:rabbitmq-host -d producer:v1
```

### Monitoring
Check the following urls of producer service, verify the behavior
 - http://localhost:5001/
 - http://localhost:5001/temperature/60
 - http://localhost:5001/temperature/101

Check the rabbitmq dashboard, verify the behavior
 - http://localhost:15672/#/

## Step 3: Set up Redis
### Bring up Redis
Fetch a docker contains redis remotely 
```
docker pull redis:latest
```
Create a container. -d means run as daemon. -p means the port
```
docker run --name redis -p 6379:6379 -d redis:latest
```

### Verification
Check if redis container exists
```
docker container ls
```
Check the redis directly from docker container.
```
docker exec -ti <container_id> /bin/bash
```

## Step 4: Set up Consumer
Reference: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

### Bring up Consumer
```
docker build -t consumer:v1 .
```

To run the consumer in docker and open browser at localhost:5000 to view the web app
```
docker run --link rabbitmq:rabbitmq-host --link redis:redis-host -d consumer:v1
```

### Verification
Check the data in redis
```
docker exec -ti <container_id> /bin/bash
```

Check the rabbitmq dashboard
 - http://localhost:15672/#/

## Step 5: Set up Dashboard

### Bring up Dashboard
```
docker build -t dashboard:v1 .
```

To run the consumer in docker and open browser at localhost:5001 to view the dashboard api
```
docker run -p 5001:5001 --link redis:redis-host -d --name dashboard dashboard:v1
```

### Verfication
http://localhost:5001/


## Step 6: Dockercompose to organize above services together
```
docker-compose up -d
```
