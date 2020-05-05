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
### Deployment instructions.
Deployment instructions can be found in [instructions](Instructions/deploy_instruction.md).