# Players leaderboard microservice.
## RabbitMQ, Django, PostgreSQL.
Microservice that builds leaderboards based on player rating. Information on the current ranking of players comes in AMQP.

Message to microservice comes in JSON: {“user_id”: int, “rating”: float, “datetime”: int<timestamp>}.
<br>
Leaderboard generated  by [Materialized View](https://postgrespro.ru/docs/postgrespro/9.5/rules-materializedviews) 
PostgreSQL (the higher the player’s rating, the higher position in the leaderboard).

The service implemented three endpoints:
1) Getting a list of all players in descending order of position in the leaderboard;
2) Getting a list of players based on the passed user_id in the request;
3) Getting a specific player, as well as neighbors standing next to him in leaderboard (top and bottom).

### Microservice architecture.
![Microservice architecture](Instructions/micro_architecture.png)
## Deployment instructions.
Deployment instructions can be found in [instructions](Instructions/deploy_instruction.md).


## Docker desription.

### Compose files
Docker compose files allow the specification of complex configurations of multiple inter-dependent
services to be run together as a cluster of docker containers. Consult the excellent docker-compose
[reference](https://docs.docker.com/compose/compose-file/) to learn about the many different
configurable settings. Compose files are written in [`.yaml`](http://yaml.org/) format and feature three
top level keys: services, volumes, and networks. Each service in the services section defines a 
separate docker container with a configuration which is independent of other services.

Here's the content of the `docker-compose.yaml` file
```YAML
# docker-compose.yml

version: '3'

services:
  db:
    image: postgres:latest
    container_name: postgres
    volumes:
      - ./postgres/create_db.sql:/docker-entrypoint-initdb.d/create_db.sql
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    networks:
      - main

  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq
    hostname: rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: "admin"
      RABBITMQ_DEFAULT_PASS: "admin"
    volumes:
      - ./rabbitmq/rabbitmq.config:/etc/rabbitmq/rabbitmq.config:ro
    networks:
      - main
    ports:
      - "5672:5672"
      - "15672:15672"

  microservice:
    build: .
    image: lut1k/microservice:latest
    container_name: microservice
    command: sh -c "sleep 30; python manage.py migrate --no-input && python manage.py runserver 0.0.0.0:8000;"
    env_file:
      - variables.env
    ports:
      - "8000:8000"
    networks:
      - main
    depends_on:
      - db
      - rabbitmq

  refresh_leaderboardview:
    image: lut1k/microservice:latest
    container_name: refresh_leaderboardview
    command: sh -c "sleep 60; python manage.py refresh_leaderboardview;"
    env_file:
      - variables.env
    depends_on:
      - db
    networks:
      - main
    restart: on-failure

  receive_messages:
    image: lut1k/microservice:latest
    container_name: receive_messages
    command: sh -c "sleep 45; python manage.py receive_messages"
    env_file:
      - variables.env
    networks:
      - main
    depends_on:
      - db
      - rabbitmq

networks:
  main:
```
###### _services_
This compose file defines five distinct services which each have a single responsibility (this is
the core philosophy of Docker): `db`, `rabbitmq`, `microservice`, `refresh_leaderboardview`, and `receive_messages`.
The `microservice` service is the central component of the Django application responsible for processing user
requests and doing whatever it is that the Django app does. The Docker image `lut1k/microservice:latest` used by the
`microservice` service is built from the [`Dockerfile`](./Dockerfile) in this project. For details of how to
write a `Dockerfile` to build a container image, see the
[docs](https://docs.docker.com/engine/reference/builder/). The `postgres` service provides the
database used by the Django app and `rabbitmq` acts as a message broker, distributing tasks in the
form of messages from the app to the celery workers for execution. The `refresh_leaderboardview` process is responsible for updating
data in a [materialized view PostgreSQL](https://www.postgresql.org/docs/10/rules-materializedviews.html). In this 
materialized view, the player’s position is determined by the player’s rating. The `receive_messages` process is responsible 
for receiving data from the AMQP queue and saving data to the database.
###### _networks_
Because all the services belong to the same `main` network defined in the `networks` section, they
are able to find each other on the network by the relevant `hostname` and communicate with each other on
any ports exposed in the service's `ports` or `expose` sections. The difference between `ports` and
`expose` is simple: `expose` exposes ports only to linked services on the same network; `ports` exposes ports
both to linked services on the same network and to the host machine (either on a random host port or on a
specific host port if specified).

**Note**: When using the `expose` or `ports` keys, **always** specify the ports using strings
enclosed in quotes, as ports specified as numbers can be interpreted incorrectly when the compose
file is parsed and give unexpected (and confusing) results!

###### _volumes_
The short syntax uses the generic [SOURCE:]TARGET[:MODE] format, where SOURCE can be either a host path or volume name. 
TARGET is the container path where the volume is mounted. Standard modes are ro for read-only and rw for read-write (default).
 
```YAML
services:
  postgres:
    volumes:
      - ./postgres/create_db.sql:/docker-entrypoint-initdb.d/create_db.sql
  rabbitmq:
    volumes:
      - ./rabbitmq/rabbitmq.config:/etc/rabbitmq/rabbitmq.config:ro
```

The `postgres` service uses the` volume` instruction to add the sql scripts `create_db.sql` to the directory
`/docker-entryPoint-initdb.d/` (see documentation [Docker Official Image](https://hub.docker.com/_/postgres)).

```SQL
#create_db.sql
CREATE DATABASE microservice_leaderboard;
CREATE ROLE microservice_user WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE microservice_leaderboard TO microservice_user;
ALTER USER microservice_user WITH LOGIN;
```

### Service dependency and startup order
The compose file allows dependency relationships to be specified between containers using the
`depends_on` key. In the case of this project, the `microservice` service depends on the `db` service
(to provide the database) as well as the `rabbitmq` service (to provide the message broker). In
practice this means that when running `docker-compose up microservice`, or just `docker-compose up`, the
`db` and `rabbitmq` services will be started if they are not already running before the `microservice`
service is started.

```YAML
services:
  microservice:
    depends_on:
      - db
      - rabbitmq
```

Unfortunately, specifying `depends_on` is not sufficient on its own to ensure the correct/desired
start up behaviour for the service cluster. This is because Docker starts the `microservice` service once
both the `db` and `rabbitmq` services have _started_; however, just because a service has
_started_ does not guarantee that it is _ready_. It is not possible for Docker to determine when
services are _ready_ as this is highly specific to the requirements of a particular service/project.
If the `microservice` service starts before the `db` service is ready to accept connections on port
5432 then the `microservice` will crash.

To solve this problem, the `microservice`,` refresh_leaderboardview`, and `receive_messages` service commands
start late: `command: sh -c "sleep 30; python manage.py migrate --no-input && python manage.py runserver 0.0.0.0:8000;"`