FROM python:3.12
RUN apt-get update && apt-get install -y wait-for-it

RUN mkdir /code
WORKDIR /code

ADD ./requirements.txt /code/

RUN pip install -r requirements.txt
