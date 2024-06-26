FROM python:3.12.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
COPY ./.env.docker /usr/src/app/.env
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app
