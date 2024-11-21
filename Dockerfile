FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

USER 1001
COPY bot.py .
COPY data .
COPY BOT_TOKEN .
CMD ["python", "bot.py"]