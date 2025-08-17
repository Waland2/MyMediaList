FROM python:3.10.12

COPY . /app

COPY requirements.txt /app

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
