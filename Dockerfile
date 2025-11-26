FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot.py .
COPY data/ data/
COPY thumbsup/ thumbsup/
COPY pingroles.json .

CMD ["python", "bot.py"]
