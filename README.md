# Toronto Public Library Feed
#### Expirementing with WebSockets, Python, and the toronto public library <br>

This project connects to the toronto public library web socket broadcasting Realtime Feed of Searches and stores the data in a postgres table.

For more info on the feed:

https://opendata.tpl.ca/

#### Quickstart with docker:

```docker
docker-compose up -d
```

Once services are up and running, view incoming data:

```docker
docker-compose logs -f -t
```

To explore the data, find the running container id using:

```docker
docker ps -a
```

Then enter the container:

```docker
docker exec -it <<YOUR_CONTAINER_ID>> /bin/bash
```

To enter the database as non-root user:

```bash
psql -U postgres
```

Select 5 rows:

```psql
SELECT * FROM tpl_searches LIMIT 5;
```


### Where can i learn more about the script itself?

The repo [here](https://github.com/oliver006/sockpuppet) has an indepth explanation of the actual socket script.