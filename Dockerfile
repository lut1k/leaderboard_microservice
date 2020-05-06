FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#postgres
COPY /postgres/create_db.sql /docker-entrypoint-initdb.d/