FROM python:3.9-slim-buster

WORKDIR /app

COPY index.html .
COPY server.py .

USER nobody

CMD ["python3", "server.py"]