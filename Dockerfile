FROM python:3.8-bullseye

RUN apt update -y
RUN apt install -y python3-pip

RUN pip3 install pandas
RUN pip3 install psycopg2
RUN pip3 install sqlalchemy

WORKDIR /app

ADD app.py /app
ADD data.csv /app

CMD ["python3", "./script.py"]