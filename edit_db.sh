#!/bin/bash
cd migrations
alembic revision --autogenerate -m "Initial"
alembic upgrade head

cd ..
sqlite3 database/main_database.db "INSERT INTO users (username, password) VALUES ('developer@mail.ru', 'password');"