FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt

CMD ["fastapi", "dev", "/app/main.py", "--host", "0.0.0.0", "--port", "8080", "--reload"]
