FROM python:3.9-slim

LABEL author="Felipe"
LABEL description="A dockerfile for Web Algorithmic Trade with Python"

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install -r /app/requirements.txt

COPY ./data/forex.db /data/forex.db 

WORKDIR /app
CMD ["python3", "main.py"]