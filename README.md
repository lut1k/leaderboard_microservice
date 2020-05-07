# Players leaderboard microservice.
## RabbitMQ, Django, PostgreSQL.
Microservice that builds leaderboards based on player rating. Information on the current ranking of players comes in AMQP.

Message to microservice comes in JSON: {“user_id”: int, “rating”: float, “datetime”: int<timestamp>}.
<br>
Leaderboard generated  by [Materialized View](https://postgrespro.ru/docs/postgrespro/9.5/rules-materializedviews) PostgreSQL (the higher the player’s rating, the
higher position in the leaderboard).

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

  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq
    hostname: rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: "admin"
      RABBITMQ_DEFAULT_PASS: "admin"
    volumes:
      - ./rabbitmq/rabbitmq.config:/etc/rabbitmq/rabbitmq.config:ro
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
    restart: on-failure

  receive_messages:
    image: lut1k/microservice:latest
    container_name: receive_messages
    command: sh -c "sleep 45; python manage.py receive_messages"
    env_file:
      - variables.env
    depends_on:
      - db
      - rabbitmq

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
form of messages from the app to the celery workers for execution.