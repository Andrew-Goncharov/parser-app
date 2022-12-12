FROM python:3.9

WORKDIR parser

COPY . .

RUN apt-get -y update

RUN apt-get -y upgrade

RUN apt-get install -y sqlite3 libsqlite3-dev

RUN pip3 install -r requirements.txt

RUN python3 -m database.create_db

RUN bash edit_db.sh

EXPOSE 9000

ENTRYPOINT ["python3", "-m", "app.main"]
