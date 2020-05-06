-- TODO брать хардкодные переменные, и добавить их из variables.env
CREATE DATABASE microservice_leaderboard;
CREATE ROLE microservice_user WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE microservice_leaderboard TO microservice_user;
ALTER USER microservice_user WITH LOGIN;