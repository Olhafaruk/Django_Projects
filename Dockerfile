FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev && apt-get clean

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

 # Явно указываем файлы
COPY entrypoint.sh /app/
COPY wait-for-db.sh /app/
RUN chmod +x /app/entrypoint.sh /app/wait-for-db.sh

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]