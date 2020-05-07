# Instructions for starting a microservice.
### I. Deploying a microservice on Ubuntu 18.04.

1.For the microservice to work properly, the following components must be installed on the machine:
- Python (I used version 3.8) [Python](https://www.python.org/);
- Message broker – [RabbitMQ](https://www.rabbitmq.com/);
- Database – [PostgreSQL](https://www.postgresql.org/);
- WEB framework – [Django](https://www.djangoproject.com/),
- [Django REST Framework](https://www.django-rest-framework.org/);


For the micro service to work, you must [install](https://www.postgresql.org/download/) PostgreSQL and [install](https://www.psycopg.org/) psycopg2 on the computer. 
Next, create the database and user in PostgreSQL.
```PostgreSQL
#CREATE DATABASE microservice_leaderboard;
#CREATE ROLE microservice_user WITH ENCRYPTED PASSWORD ‘password’;
#GRANT ALL PRIVILEGES ON DATABASE microservice_leaderboard TO microservice_user;
#ALTER USER microservice_user WITH LOGIN;
```

2.Also, for the microservice to work, you must [install](https://www.rabbitmq.com/download.html) RabbitMQ. 
To work with RabbitMQ you need to create a user and activate the rabbitmq_management plugin:
```RabbitMQ
#rabbitmq-plugins enable rabbitmq_management
#rabbitmqctl add_user admin admin
#rabbitmqctl set_user_tags admin administrator
#rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
```

3.Next, you need to clone the repository.

`$git clone https://github.com/lut1k/leaderboard_microservice.git`

4.Create a virtual environment for the project.

`$python3 –m venv venv`

5.The application uses environment variables. You must modify the venv/bin/activate file and add the following variables to the end of the file:

```
$vim venv/bin/activate

export DB_NAME=microservice_leaderboard
export DB_USER=microservice_user
export DB_PASSWORD=password
export AMQP_USER=admin
export AMQP_PASSWORD=admin
```

6.Activate the virtual environment and install the dependencies from the requirements.txt file

```
$source venv/bin/activate
$pip install -r requirements.txt
```

7.To create the necessary tables and materialized view in the database, you must run the following command:

`$python manage.py migrate`

8.The following manage.py file commands are used to start and operate the microservice, which must be run in different processes:

- `$python manage.py receive_messages` - starts the consumer in AMQP, receives messages and sends them to the database;
- `$python manage.py refresh_leaderboard` - starts the update process Materialized View PostgreSQL;
- `$python manage.py runserver` - starts a lightweight development Web server on the local machine. By default, the server runs on port 8000 on the IP address 127.0.0.1. You can pass in an IP address and port number explicitly.

9.The project also has an imitation of the AMQP producer, it can be launched in a separate process to send messages to RabbitMQ:

`$python producer/mocksender.py`

10.The result of the work can be seen at the URL: yourhost:8000/leaderboard/players.

### II. Deploying a microservice with [Docker](https://www.docker.com/).

In process ...