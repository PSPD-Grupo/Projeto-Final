FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    rm -rf /var/lib/apt/lists/*

COPY proto ./proto
COPY src ./src

RUN python -m grpc_tools.protoc \
    -I proto \
    --python_out=src/generated \
    --grpc_python_out=src/generated \
    proto/patient_data.proto

EXPOSE 50052 8081

CMD ["python", "-m", "app.main"]
