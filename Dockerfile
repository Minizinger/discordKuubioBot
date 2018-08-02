FROM python:3
ADD . /code
WORKDIR /code/bot
RUN pip3 install -r requirements.txt