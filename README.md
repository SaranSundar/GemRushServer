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