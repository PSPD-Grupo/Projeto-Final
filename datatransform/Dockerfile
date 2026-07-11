FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
COPY proto/ proto/
COPY src/ src/
RUN pip install --no-cache-dir --target=/build/deps -r requirements.txt grpcio-tools
RUN touch proto/__init__.py
RUN python -m grpc_tools.protoc \
    -I proto \
    --python_out=proto \
    --grpc_python_out=proto \
    proto/datatransform.proto

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /build/deps /usr/local/lib/python3.11/site-packages
COPY --from=builder /build/src ./src
COPY --from=builder /build/proto ./proto
ENV PYTHONPATH=/app/src:/app/proto
EXPOSE 50053 9103
CMD ["python", "-m", "server"]