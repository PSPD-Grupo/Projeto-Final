VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

PROTO_DIR := proto

.PHONY: venv install proto run test test-unit test-integration lint clean docker-build docker-up

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

## Gera os stubs Python a partir do .proto, direto dentro de proto/
proto:
	touch $(PROTO_DIR)/__init__.py
	$(PYTHON) -m grpc_tools.protoc \
		-I $(PROTO_DIR) \
		--python_out=$(PROTO_DIR) \
		--grpc_python_out=$(PROTO_DIR) \
		--pyi_out=$(PROTO_DIR) \
		$(PROTO_DIR)/datatransform.proto
	@echo "Stubs gerados em $(PROTO_DIR)"

## Sobe o servidor localmente
run:
	PYTHONPATH=src:proto JWT_SECRET=dev-secret PSEUDONYMIZE_SALT=dev-salt \
		$(PYTHON) -m server

test:
	$(PYTHON) -m pytest --cov=src --cov-report=term-missing

test-unit:
	$(PYTHON) -m pytest tests/unit -v

test-integration:
	$(PYTHON) -m pytest tests/integration -v

lint:
	$(PYTHON) -m pyflakes src

clean:
	rm -f $(PROTO_DIR)/datatransform_pb2*.py $(PROTO_DIR)/datatransform_pb2*.pyi
	find . -type d -name __pycache__ -exec rm -rf {} +

docker-build:
	docker build -t data-transform-service:latest .

docker-up:
	docker compose up --build