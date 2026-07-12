#!/usr/bin/env bash
# Gera os stubs gRPC dentro de proto/ e corrige o import absoluto
# que o protoc gera por padrão (auth_pb2_grpc.py importa auth_pb2
# como módulo top-level, o que quebra quando proto/ é um pacote).
set -e

python -m grpc_tools.protoc \
  -I=./proto \
  --python_out=./proto \
  --pyi_out=./proto \
  --grpc_python_out=./proto \
  ./proto/auth.proto

# Corrige "import auth_pb2 as auth__pb2" -> "from . import auth_pb2 as auth__pb2"
sed -i 's/^import auth_pb2 as auth__pb2$/from . import auth_pb2 as auth__pb2/' \
  ./proto/auth_pb2_grpc.py

echo "Stubs gerados e imports corrigidos em ./proto/"