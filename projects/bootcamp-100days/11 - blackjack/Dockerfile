FROM python:3.10-slim

LABEL author="Felipe"
LABEL description="A dockerfile for game Blackjack with Python"

RUN mkdir /app/
WORKDIR /app/

COPY ./src /app/

WORKDIR /app/

CMD ["python3", "blackjack.py"]