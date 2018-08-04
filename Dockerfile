FROM python:3.6-slim
ADD . /code
WORKDIR /code/bot
RUN pip3 install -r requirements.txt