# GemRushServer

Instructions to start server

```
# Only need to build once

docker build -t compose-flask .

# After server is running, any changes to the code will auto redeploy

docker-compose up
```

Instructions to stop server

```
docker-compose down
```

Instructions to view server / health check

```
visit http://0.0.0.0:9375/
```

Instructions to destroy docker
```
docker system prune -a -f --volumes
```

Instructions to clean start
```
docker-compose down && docker system prune -a -f --volumes && docker build -t compose-flask . && docker-compose up
```