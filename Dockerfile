FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x boot.sh

ENV FLASK_APP app

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
