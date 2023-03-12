FROM python:3.11-slim

LABEL author="Felipe"
LABEL description="A dockerfile for Web Algorithmic Trade with Python"

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install -r /app/requirements.txt

WORKDIR /app
CMD ["python3", "scrape.py"]