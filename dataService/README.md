# Patient Data Service

Microserviçoo para consulta de dados de pacientes no PostgreSQL

Ele expoe:

- servidor gRPC para o API Gateway;
- servidor FastAPI apenas para health/readiness;
- acesso ao banco via variaveis de ambiente;
- autorização de dominio baseada no contexto repassado pelo Gateway.

## Arquitetura

```text
Frontend
  -> API Gateway
      -> Patient Data Service gRPC
          -> PostgreSQL
```

O API Gateway deve validar o token do usuario e repassar contexto para o
Patient Data Service via metadata gRPC:

```text
x-user-username: nome_do_usuario
x-user-roles: ADMIN,DOCTOR
x-user-scopes: patient:read,patient:read:all
x-request-id: identificador_da_requisicao
```

Usuarios com `patient:read:all` ou role `ADMIN` conseguem consultar todos os
pacientes. Os demais usuarios so consultam pacientes com vinculo ativo em
`user_patient_assignments`.

## Configuracao

Copie a `.env.example` para `.env` e faça os ajustes, por exemplo:

```text
DB_HOST=192.168.500000.5
DB_PORT=948732984732
DB_NAME=pseudopep_g08875648736
DB_USER=grupo08_user
DB_PASSWORD=coxinha123
```

## Executando localmente

Instale as dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Gere os arquivos Python do contrato gRPC, se quiser fazer isso manualmente:

```bash
python -m grpc_tools.protoc -I proto --python_out=src/generated --grpc_python_out=src/generated proto/patient_data.proto
```

O servico tambem tenta gerar esses arquivos automaticamente ao iniciar, caso
eles ainda nao existam.

Suba o servico:

```bash
$env:PYTHONPATH = "src"
python -m app.main
```

Por padrao:

- gRPC: `0.0.0.0:50051`
- FastAPI health: `0.0.0.0:8080`

## Endpoints gRPC

Serviço: `patientdata.PatientDataService`

- `HealthCheck`
- `GetPatient`
- `SearchPatients`
- `ListEncounters`
- `ListClinicalEvents`

## Build Docker

```bash
docker build -t patient-data-service .
docker run --env-file .env -p 50051:50051 -p 8080:8080 patient-data-service
```

## Observaçao sobre segurança!!!!!!!

Este microservico nao valida o JWT diretamente. A autenticacao principal fica
no API Gateway/Auth Service. Mesmo assim, ele aplica uma regra minima de
autorizacao de dominio usando `user_patient_assignments`.
