#!/bin/bash

 # Ждем, пока база данных станет доступна.
 # Предполагается, что заданы переменные окружения PG_HOST и PG_PORT.
while ! nc -z "$PG_HOST" "$PG_PORT"; do
  echo "Waiting for database connection at $PG_HOST:$PG_PORT..."
  sleep 1
done

echo "Database is up - continuing."