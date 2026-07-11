FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./app /app/app/
COPY ./proto /app/proto
COPY ./.env_docker /app/.env
COPY ./requirements.txt /app/


RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 50051

CMD ["python", "-m", "app"]
