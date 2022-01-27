FROM python:3.9-slim

LABEL author="Felipe"
LABEL description="A dockerfile for Algorithmic Trade with Python"

RUN mkdir /app/
WORKDIR /app/

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./src /app/
COPY ./data/forex.db /data/forex.db
COPY ./data/commodities.db /data/commodities.db 

WORKDIR /app/
CMD ["python3", "data.py"]

