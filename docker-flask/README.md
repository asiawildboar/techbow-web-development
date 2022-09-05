### Docker flask quick deployment commands overview

To build the image
```
docker build -t web .
```

To check the image we just build
```
docker image ls
```

To delete the image
```
docker rmi <image_id>
```

To run the flask app in docker and open browser at localhost:5000 to view the web app
```
docker run -p 5001:5001 -d web
```
  
To check the container of the flask app
```
docker container ls
```

To check the status of the container
```
docker container ls
```

To go into the container 
```
docker exec -ti <container_id> /bin/bash
```

To delete the container
```
docker rm <container_id>
```
