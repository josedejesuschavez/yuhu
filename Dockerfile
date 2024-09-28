FROM python:3.12

RUN mkdir /code
WORKDIR /code

ADD ./requirements.txt /code/

RUN pip install -r requirements.txt
